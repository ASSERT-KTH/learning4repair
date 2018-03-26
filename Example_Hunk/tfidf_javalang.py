import re
import math
import os
import glob
import random
import getopt
import sys
import operator
import javalang
import numpy as np

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print "tfidf_javalang.py -k <Top k prediction>"
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print "tfidf_javalang.py -k <Top k prediction>"
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()

    path_files = "../Files_Hunk"
    for filename in glob.glob(os.path.join(path_files, "*.txt")):
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

            # TF of inserted tokens
            insert_dict_tf = {}
            try:
                for token in insert_tokens:
                    if(token.value in insert_dict_tf):
                        insert_dict_tf[token.value] += 1
                    else:
                        insert_dict_tf[token.value] = 1
            except javalang.tokenizer.LexerError:
                continue

            # Rest are the program
            lines = lines[insert_end+1:]
            program_length = len(lines)
            lines = "".join(lines)
            program_tokens = javalang.tokenizer.tokenize(lines)

            program_dict_tf = [{} for _ in range(0, program_length)]
            # Compute TF for each line in the program
            try:
                for token in program_tokens:
                    # Row starts from 1
                    (row, col) = token.position
                    if(token.value in program_dict_tf[row-1]):
                        program_dict_tf[row-1][token.value] +=1
                    else:
                        program_dict_tf[row-1][token.value] = 1
            except javalang.tokenizer.LexerError:
                continue

            # IDF for inserted tokens
            insert_token_idf = {}
            for token in insert_dict_tf:
                count = 0
                for i in range(0, program_length):
                    if token in program_dict_tf[i]:
                        count+=1
                if(count == 0):
                    insert_token_idf[token] = math.log(program_length)
                else:
                    insert_token_idf[token] = math.log(program_length/(count*1.0))

            # TF-IDF vector for inserted tokens
            insert_weight = []
            for token in insert_dict_tf:
                insert_weight.append(insert_dict_tf[token]*insert_token_idf[token])
            insert_weight = normalize(insert_weight)

            # Precompute tfidf for each line
            tfidf_vectors = np.zeros(shape=(program_length, len(insert_weight)))
            for i in range(0, program_length):
                tfidf_vec = []
                for token in insert_dict_tf:
                    if(token in program_dict_tf[i]):
                        tf=program_dict_tf[i][token]
                        idf=insert_token_idf[token]
                        tfidf_vec.append(tf*idf)
                    else:
                        tfidf_vec.append(0)
                tfidf_vectors[i] = tfidf_vec

            # Only looking for hunk with similar size
            max_diff = insert_length
            score = {}
            # Sum up tfidf for the hunk and compare
            for i in range(0, program_length+1):
                for j in range(i+1, program_length+1):
                    if(j-i > max_diff):
                        break
                    vec = np.zeros(shape=(len(insert_weight)))
                    for n in range(i,j):
                        vec = vec + tfidf_vectors[i]
                    vec = normalize(vec)
                    score[(i+1,j)] = cosine_sim(insert_weight, vec)

            # First we compare cosine similarity, then we compare hunk size
            score_cmp = lambda ((s1, e1), v1), ((s2,e2), v2):cmp((v1, e2-s2), (v2, e1-s1))
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
