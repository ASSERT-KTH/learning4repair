import re
import math
import os
import glob
import random
import getopt
import sys
import javalang
import numpy as np

k = 1

def main(argv):
    global k
    chosen_datasets = None
    try:
        opts, args = getopt.getopt(argv, "hd:k:")
    except getopt.GetoptError:
        print("tfidf_javalang.py -k <Top k prediction> -d <Paths to datasets>")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("tfidf_javalang.py -k <Top k prediction> -d <Paths to datasets>")
            sys.exit()
        elif opt == "-k":
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()
        elif opt == "-d":
            chosen_datasets = arg.split(":")

    if(chosen_datasets):
        for path_to_dataset in chosen_datasets:
            path_to_tasks = os.path.join(path_to_dataset, "Tasks/")
            for task in os.listdir(path_to_tasks):
                if(task.endswith(".txt")):
                    path_to_task = os.path.abspath(os.path.join(path_to_tasks, task))
                    predict(path_to_task)
    else:
        path_to_current = os.path.abspath(os.path.dirname(__file__))
        path_to_datasets = os.path.join(path_to_current, "../Datasets/")

        for dataset_dir in os.listdir(path_to_datasets):
            path_to_dataset = os.path.join(path_to_datasets, dataset_dir)
            if(os.path.isdir(path_to_dataset)):
                path_to_tasks = os.path.join(path_to_dataset, "Tasks/")
                for task in os.listdir(path_to_tasks):
                    if(task.endswith(".txt")):
                        path_to_task = os.path.abspath(os.path.join(path_to_tasks, task))
                        predict(path_to_task)


def predict(path_to_task):
    global k
    with open(path_to_task, 'r') as file:
        lines = file.readlines()

        # First line is the inserted line
        insert = lines[0]
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
            return

        # Rest are the program
        lines = lines[2:]
        program_length = len(lines)
        lines_string = "".join(lines)
        program_tokens = javalang.tokenizer.tokenize(lines_string)

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
            return

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

        # Comput cosine similarity with each line
        score = np.zeros(shape=(program_length))
        for i in range(0, program_length):
            program_line_weight = []
            for token in insert_dict_tf:
                if(token in program_dict_tf[i]):
                    tf=program_dict_tf[i][token]
                    idf=insert_token_idf[token]
                    program_line_weight.append(tf*idf)
                else:
                    program_line_weight.append(0)
            program_line_weight = normalize(program_line_weight)
            if(''.join(insert.split()) == ''.join(lines[i].split())):
                score[i] = 0
            else:
                score[i] = cosine_sim(insert_weight,program_line_weight)

        # Select top k result and print
        guess = score.argsort()[-k:][::-1]
        guess_string = ""
        for ind in guess:
            guess_string = guess_string + str(ind+1) + " "

        print(path_to_task + " " + guess_string)

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
