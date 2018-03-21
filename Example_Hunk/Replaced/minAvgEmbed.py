import tensorflow as tf
import numpy as np
import pickle
import os
import glob
import javalang
from scipy import spatial
import random
import re
import sys
import getopt
import math

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print "minAvgEmbed.py -k <Top k prediction>"
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print "minAvgEmbed.py -k <Top k prediction>"
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()

    os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
    np.warnings.filterwarnings('ignore')

    tf.reset_default_graph()

    with open("Embedding_100000files_10000vol/dictionary.pickle" , "rb") as f:
        [count,dictionary,reverse_dictionary,vocabulary_size] = pickle.load(f)

    embedding_size = 32

    #embeddings = tf.get_variable(VARIABLE,[DIMENSION], INIT)
    embeddings = tf.get_variable("Variable"
        ,[vocabulary_size, embedding_size], initializer = tf.zeros_initializer)
    nce_weights = tf.get_variable("Variable_1"
        ,[vocabulary_size, embedding_size], initializer = tf.zeros_initializer)
    nce_biases = tf.get_variable("Variable_2"
        ,[vocabulary_size], initializer = tf.zeros_initializer)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, "Embedding_100000files_10000vol/model.ckpt")
        embed = embeddings.eval()

    path_file = "../../Files_Hunk/Replaced"
    for filename in glob.glob(os.path.join(path_file, "*.txt")):
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Get last line of inserted code
            for i in range(0,len(lines)):
                if(lines[i].startswith("@@@")):
                    insert_end = i
                    break

            # Get inserted code hunk
            insert = lines[:insert_end]
            insert_length = len(insert)
            insert = "".join(insert)
            insert_tokens = javalang.tokenizer.tokenize(insert)

            # Compute avg embedding for inserted hunk
            try:
                insert_avg_embed = np.zeros(shape=(embedding_size))
                tokenCount = 0
                for token in insert_tokens:
                    token_embedding = embed[dictionary.get(token.value, 0)]
                    insert_avg_embed += token_embedding
                    tokenCount += 1
                if(tokenCount == 0):
                    continue
                else:
                    insert_avg_embed = insert_avg_embed/tokenCount
                    insert_avg_embed = normalize(insert_avg_embed)
            except javalang.tokenizer.LexerError:
                continue

            # The rest is the program
            lines = lines[insert_end+1:]
            program_length = len(lines)
            lines = "".join(lines)
            program_tokens = javalang.tokenizer.tokenize(lines)

            # Compute avg embedding for each line
            program_embed_vectors = np.zeros(shape=(program_length, embedding_size))
            try:
                tokenCount = 0
                old_row = 1
                for token in program_tokens:
                    token_embedding = embed[dictionary.get(token.value, 0)]
                    (row, col) = token.position
                    if(row == old_row):
                        tokenCount+=1
                        program_embed_vectors[row-1] += token_embedding
                    else:
                        if(not tokenCount == 0):
                            program_embed_vectors[old_row-1] = program_embed_vectors[old_row-1]/(tokenCount*1.0)
                        program_embed_vectors[row-1] += token_embedding
                        old_row = row
                        tokenCount = 1
                program_embed_vectors[row-1] = program_embed_vectors[row-1]/(tokenCount*1.0)
            except javalang.tokenizer.LexerError:
                continue

            # Only consider hunk with similar size
            max_diff = insert_length
            score = {}
            # Compute avg embedding for each hunk
            # And compute cosine similarity
            for i in range(0, program_length+1):
                for j in range(i+1, program_length+1):
                    if(j-i > max_diff):
                        break
                    hunk_avg_embed = np.zeros(shape=(embedding_size))
                    for n in range(i,j):
                        hunk_avg_embed += program_embed_vectors[n]
                    hunk_avg_embed = hunk_avg_embed/(1.0*(j-i))
                    if(not hunk_avg_embed.any()):
                        continue
                    hunk_avg_embed = normalize(hunk_avg_embed)
                    score[(i+1,j)] = cosine_sim(insert_avg_embed, hunk_avg_embed)

            # First we compare cosine similarity, then we compare hunk size
            score_cmp = lambda ((s1,e1), v1), ((s2,e2), v2):cmp((v1, e2-s2), (v2, e1-s1))
            sorted_score = sorted(score.items(), cmp=score_cmp, reverse=True)

            guess_string = ""
            for i in range(0,min(k, len(sorted_score))):
                guess_string = guess_string + str(sorted_score[i][0][0]) + " " + str(sorted_score[i][0][1]) + " "

            print(os.path.basename(filename) + " " + guess_string)

def cosine_sim(w1,w2):
    if(sum(w1) == 0 or sum(w2) == 0):
        return 0
    score = 0
    d1 = 0
    d2 = 0
    for i in range (0, len(w1)):
        score += w1[i]*w2[i]
        d1+=w1[i]**2
        d2+=w2[i]**2
    return score/(math.sqrt(d1)*math.sqrt(d2))

def normalize(w):
    s = sum(w)
    if(s == 0):
        return [0]*len(w)
    new_w = []
    for weight in w:
        new_w.append(weight/s)
    return new_w

if __name__=="__main__":
    main(sys.argv[1:])
