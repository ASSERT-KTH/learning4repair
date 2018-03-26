import tensorflow as tf
import numpy as np
import pickle
import os,glob
import javalang
import random
import re
import sys
import getopt
import operator
import math
from scipy.spatial import distance

def main(argv):
    #http://proceedings.mlr.press/v37/kusnerb15.pdf
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print "minEmbedDistance.py -k <Top k prediction>"
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print "minEmbedDistance.py -k <Top k prediction>"
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

    path_files = "../Files_Hunk"
    for abc in range(4895,4896):
        filename = path_files+"/"+str(abc)+".txt"
    #for filename in glob.glob(os.path.join(path_files, "*.txt")):
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

            # Calculate the avg embedding
            try:
                insert_embed = []
                for token in insert_tokens:
                    if(not dictionary.get(token.value, 0) == 0):
                        insert_embed.append(embed[dictionary.get(token.value)])
                if not insert_embed:
                    continue
            except javalang.tokenizer.LexerError:
                continue

            # The rest is the program
            lines = lines[insert_end+1:]
            program_length = len(lines)
            lines = "".join(lines)
            program_tokens = javalang.tokenizer.tokenize(lines)

            # Calculate the avg embedding of each line
            program_embed_vectors = [[] for _ in range(program_length)]
            try:
                for token in program_tokens:
                    if(dictionary.get(token.value, 0) == 0):
                        continue
                    token_embedding = embed[dictionary.get(token.value)]
                    (row, col) = token.position
                    program_embed_vectors[row-1].append(token_embedding)
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
                    hunk_embed = []
                    for n in range(i,j):
                        hunk_embed = hunk_embed+program_embed_vectors[n]
                    score[(i+1,j)] = min_cum_distance(insert_embed, hunk_embed)

            # First we compare cosine similarity, then we compare hunk size
            score_cmp = lambda ((s1,e1), v1), ((s2,e2), v2):cmp((v1, e1-s1), (v2, e2-s2))
            sorted_score = sorted(score.items(), cmp=score_cmp)


            guess_string = ""
            for i in range(0,min(k, len(sorted_score))):
                guess_string = guess_string + str(sorted_score[i][0][0]) + " " + str(sorted_score[i][0][1]) + " "

            print(os.path.basename(filename) + " " + guess_string)

def min_cum_distance(insert_embed, program_embed):
    score = 0
    for i in range(0, len(insert_embed)):
        min_distance = float('Inf')
        for j in range(0, len(program_embed)):
            d = distance.euclidean(insert_embed[i],program_embed[j])
            if(d < min_distance):
                min_distance = d
        score += min_distance
    return score

if __name__=="__main__":
    main(sys.argv[1:])
