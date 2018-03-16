import re
import math
import os
import glob
import random
import getopt
import sys
import numpy as np

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print("tfidf.py -k <Top k prediction>")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("tfidf.py -k <Top k prediction>")
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()

    path_files = "../../Files/Replaced"
    for filename in glob.glob(os.path.join(path_files, "*.txt")):
        with open(filename, 'r') as file:
            lines = file.readlines()
            insert = filter(None,re.split("[,.();_\t\n ]",lines[0]))

            lines = lines[2:]
            for i in range(0,len(lines)):
                lines[i] = filter(None,re.split("[,.();_\t\n ]", lines[i]))

            # Assume tf is 1 in the inserted line
            weight_insert = []
            for token in insert:
                freq = 0
                for i in range(0,len(lines)):
                    if token in lines[i]:
                        freq+=1
                if(freq == 0):
                    weight_insert.append(1)
                else:
                    weight_insert.append(math.log(len(lines)/(freq*1.0)))
            weight_insert = normalize(weight_insert)

            score = np.zeros(shape=(len(lines)))
            for i in range(0, len(lines)):
                weight_delete = []
                for j in range(0, len(insert)):
                    if(insert[j] in lines[i]):
                        tf=lines[i].count(insert[j])
                        idf=weight_insert[j]
                        weight_delete.append(tf*idf)
                    else:
                        weight_delete.append(0)
                weight_delete = normalize(weight_delete)
                score[i] = cosine_sim(weight_insert,weight_delete)
            guess = score.argsort()[-k:][::-1]
            guess_string = ""
            for ind in guess:
                guess_string = guess_string + str(ind+1) + " "

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
