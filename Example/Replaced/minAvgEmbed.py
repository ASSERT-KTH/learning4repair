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

    with open("Embedding_100000files_500dict/dictionary.pickle" , "rb") as f:
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
        saver.restore(sess, "Embedding_100000files_500dict/model.ckpt")
        embed = embeddings.eval()

    path_files = "../../Files/Replaced"
    for filename in glob.glob(os.path.join(path_files, "*.txt")):
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Get inserted code
            insert = lines[0]
            insert_tokens = javalang.tokenizer.tokenize(insert)

            # Calculate the avg embedding
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
            lines = lines[2:]
            file_length = len(lines)
            lines = "".join(lines)
            program_tokens = javalang.tokenizer.tokenize(lines)

            # Calculate the avg embedding of each line
            program_embed_vectors = np.zeros(shape=(file_length, embedding_size))
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

            # Compute cosine similarity
            score = {}
            for i in range(0, file_length):
                if(not program_embed_vectors[i].any()):
                    continue
                program_embed_vectors[i] = normalize(program_embed_vectors[i])
                score[i+1] = cosine_sim(insert_avg_embed, program_embed_vectors[i])

            sorted_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

            guess_string = ""
            for i in range(0,min(k, len(sorted_score))):
                guess_string = guess_string + str(sorted_score[i][0]) + " "

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
        return np.zeros(shape=(len(w)))
    new_w = []
    for weight in w:
        new_w.append(weight/s)
    return np.array(new_w)

if __name__=="__main__":
    main(sys.argv[1:])
