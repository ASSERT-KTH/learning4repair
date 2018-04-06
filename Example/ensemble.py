import getopt
import sys
import os
import re
import math
import numpy as np
import tensorflow as tf
import pickle
import javalang
import operator
from scipy.spatial import distance

k = 1

def main(argv):
    global k
    chosen_datasets = None
    try:
        opts, args = getopt.getopt(argv, "hd:k:")
    except getopt.GetoptError:
        print("minSumEmbedAndEditDistance.py -k <Top k prediction> -d <Paths to datasets>")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("minSumEmbedAndEditDistance.py -k <Top k prediction> -d <Paths to datasets>")
            sys.exit()
        elif opt == "-k":
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()
        elif opt == "-d":
            chosen_datasets = arg.split(":")

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

    if(chosen_datasets):
        for path_to_dataset in chosen_datasets:
            path_to_tasks = os.path.join(path_to_dataset, "Tasks/")
            for task in os.listdir(path_to_tasks):
                if(task.endswith(".txt")):
                    path_to_task = os.path.abspath(os.path.join(path_to_tasks, task))
                    predict(path_to_task, embedding_size, dictionary, embed)
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
                        predict(path_to_task, embedding_size, dictionary, embed)

def predict(path_to_task, embedding_size, dictionary, embed):
    global k
    score_tfidf_split = predict_tfidf_split(path_to_task)
    score_normalized_lcsDistance = predict_normalized_lcsDistance(path_to_task)
    score_embedDistance = predict_embedDistance(path_to_task, embedding_size, dictionary, embed)
    score = {}
    for i in range(1, len(score_tfidf_split)):
        score[i]=(score_tfidf_split[i]+score_normalized_lcsDistance[i]+score_embedDistance[i])/3.0

    # Select top k result and print
    sorted_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
    guess_string = ""
    for i in range(0,min(k, len(sorted_score))):
        guess_string = guess_string + str(sorted_score[i][0]) + " "

    print(path_to_task + " " + guess_string)


def predict_tfidf_split(path_to_task):
    with open(path_to_task, 'r') as file:
        lines = file.readlines()

        insert = lines[0]
        # First line is the inserted line
        insert_tokens = filter(None,re.split("[,.();{}_\[\]\+\-\*\/&|\t\n\r ]",insert))

        # TF of inserted tokens
        insert_dict_tf = {}
        for token in insert_tokens:
            if(token in insert_dict_tf):
                insert_dict_tf[token] += 1
            else:
                insert_dict_tf[token] = 1

        # Rest are the program
        lines = lines[2:]
        program_length = len(lines)
        program_tokens = [[] for _ in range(0, program_length)]
        for i in range(0,program_length):
            program_tokens[i] = filter(None,re.split("[,.();{}_\[\]\+\-\*\/&|\t\n\r ]", lines[i]))

        program_dict_tf = [{} for _ in range(0, program_length)]
        # Compute TF for each line in the program
        for i in range(0 , program_length):
            for token in program_tokens[i]:
                if(token in program_dict_tf[i]):
                    program_dict_tf[i][token] +=1
                else:
                    program_dict_tf[i][token] = 1

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
        score = {}
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
                score[i+1] = 0
            else:
                score[i+1] = cosine_sim(insert_weight,program_line_weight)

        return score

def predict_normalized_lcsDistance(path_to_task):
    with open(path_to_task, 'r') as file:
        lines = file.readlines()

        # Get inserted code
        insert = lines[0]
        max_len = len(max(lines, key=len))

        # Rest are the program
        lines = lines[2:]
        program_length = len(lines)


        score = {}
        for i in range(0, program_length):
            if(''.join(insert.split()) == ''.join(lines[i].split())):
                score[i+1] = 0
            else:
                score[i+1] = lcs(insert, lines[i].strip())/(max_len*1.0)

        return score

# Change to split!!! TODO
def predict_embedDistance(path_to_task, embedding_size, dictionary, embed):
    with open(path_to_task, 'r') as file:
        lines = file.readlines()

        # Get inserted code
        insert = lines[0]
        insert_tokens = javalang.tokenizer.tokenize(insert)

        # The rest is the program
        lines = lines[2:]
        file_length = len(lines)
        lines_string = "".join(lines)
        program_tokens = javalang.tokenizer.tokenize(lines_string)

        # Calculate the avg embedding
        try:
            insert_embed = []
            for token in insert_tokens:
                if(not dictionary.get(token, 0) == 0):
                    insert_embed.append(embed[dictionary.get(token)])
            if not insert_embed:
                score = {}
                for i in range(0, file_length):
                    score[i+1] = 0
                return score

        except javalang.tokenizer.LexerError:
            score = {}
            for i in range(0, file_length):
                score[i+1] = 0
            return score

        program_embed_vectors = [[] for _ in range(file_length)]
        try:
            for token in program_tokens:
                if(dictionary.get(token.value, 0) == 0):
                    continue
                token_embedding = embed[dictionary.get(token.value)]
                (row, col) = token.position
                program_embed_vectors[row-1].append(token_embedding)
        except javalang.tokenizer.LexerError:
            score = {}
            for i in range(0, file_length):
                score[i+1] = 0
            return score

        # Compute cosine similarity
        score = {}
        max_score = -1
        for i in range(0, file_length):
            if(not program_embed_vectors[i]):
                score[i+1] = 0
            else:
                score[i+1] = min_cum_distance(insert_embed, program_embed_vectors[i])
                if(score[i+1] > max_score):
                    max_score = score[i+1]

        for i in range(0, file_length):
            if(not score[i+1] == 0):
                score[i+1] = 1 - score[i+1]/(max_score*1.0)

        return score

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

def lcs(X , Y):
    # From https://www.geeksforgeeks.org/longest-common-subsequence/
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None]*(n+1) for i in xrange(m+1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j] , L[i][j-1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]

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
