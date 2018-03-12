import os
import glob
import random
import sys
import getopt

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print 'randomGuess.py -k <Top k score>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'randomGuess.py -k <Top k score>'
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("Must be integer")
                raise

    path = "../../Files/Added"
    for filename in glob.glob(os.path.join(path, "*.txt")):
    # for i in range(1,100):
        # filename=path+"/"+str(i)+".txt"
        with open(filename, 'r') as file:
            length = len(file.readlines()) - 2
            guess = random.sample(list(range(0,length)), min(length, k))
            guess_string = ""
            for line in guess:
                guess_string = guess_string + str(line) + " "
            print(os.path.basename(filename) + " " + guess_string)

if __name__=="__main__":
    main(sys.argv[1:])
