import edit_distance
import math
import os
import glob
import getopt
import sys
import operator
import numpy as np

k = 1

def editDistance(s1,s2):
    return edit_distance.SequenceMatcher(a=s1, b=s2).distance()

def main(argv):
    global k
    chosen_datasets = None
    try:
        opts, args = getopt.getopt(argv, "hd:k:")
    except getopt.GetoptError:
        print("minEditDistance.py -k <Top k prediction> -d <Paths to datasets>")
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print("minEditDistance.py -k <Top k prediction> -d <Paths to datasets>")
            sys.exit()
        elif opt == "-k":
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()
        elif opt == "-d":
            chosen_datasets = arg.split(":")

    '''
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
    '''
    predict("/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition.nosync/Datasets/Dataset2/Tasks/4340.txt")


def predict(path_to_task):
    with open(path_to_task, 'r') as file:
        lines = file.readlines()

        # First line is the inserted line
        insert = lines[0]

        # Rest are the program
        lines = lines[2:]
        score = {}
        for i in range(0, len(lines)):
            score[i+1] = editDistance(lines[i].strip(),insert.strip())

        sorted_score = sorted(score.items(), key=operator.itemgetter(1))
        guess_string = ""
        for i in range(0,min(k, len(sorted_score))):
            guess_string = guess_string + str(sorted_score[i][0]) + " "
        print(path_to_task + " " + guess_string)


if __name__=="__main__":
    main(sys.argv[1:])
