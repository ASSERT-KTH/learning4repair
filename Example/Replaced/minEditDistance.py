import edit_distance
import math
import os
import glob
import getopt
import sys
import numpy as np

def editDistance(s1,s2):
    return edit_distance.SequenceMatcher(a=s1, b=s2).distance()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print "minEditDistance.py -k <Top k prediction>"
        sys.exit()
    for opt, arg in opts:
        if opt == "-h":
            print "minEditDistance.py -k <Top k prediction>"
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()

    path = "../../Files/Replaced/"
    for i in range (1,101):
        filename=path+str(i)+".txt"
        with open(filename, 'r') as file:
            lines = file.readlines()

            # First line is the inserted line
            insert = lines[0]

            # Rest are the program
            lines = lines[2:]
            score = np.zeros(shape=(len(lines)))
            for i in range(0, len(lines)):
                score[i] = editDistance(lines[i].strip(),insert.strip())

            guess = score.argsort()[:k]
            guess_string = ""
            for ind in guess:
                guess_string = guess_string + str(ind+1) + " "
            print(os.path.basename(filename) + " " + guess_string)


if __name__=="__main__":
    main(sys.argv[1:])
