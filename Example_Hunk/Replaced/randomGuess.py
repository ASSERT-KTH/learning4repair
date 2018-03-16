import random
import os
import glob
import getopt
import sys

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print "randomGuess.py -k <Top k prediction>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "randomGuess.py -k <Top k prediction>"
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("k must be integer")
                sys.exit()

    path = "../../Files_Hunk/Replaced"
    for filename in glob.glob(os.path.join(path, "*.txt")):
        with open(filename, 'r') as file:
            lines = file.readlines()

            for i in range(0,len(lines)):
                if(lines[i].startswith("@@@")):
                    insert_end = i
                    break

            insert = lines[:insert_end]
            lines = lines[insert_end+1:]
            max_diff = len(insert)

            guess_string = ""
            for i in range(0,k):
                start = random.randint(1,len(lines))
                end = min(len(lines), start+random.randint(0, max_diff))
                guess_string = guess_string + str(start) + " " + str(end) + " "

            print(os.path.basename(filename) + " " + guess_string)


if __name__=="__main__":
    main(sys.argv[1:])
