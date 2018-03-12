import edit_distance,math,os,glob,getopt,sys
import numpy as np

def editDistance(s1,s2):
    return edit_distance.SequenceMatcher(a=s1, b=s2).distance()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:")
    except getopt.GetoptError:
        print 'tfidf.py -k <Top k score>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'tfidf.py -k <Top k score>'
            sys.exit()
        elif opt in ("-k"):
            try:
                k = int(arg)
            except ValueError:
                print("Must be integer")
                raise

    path = "../../Files/Replaced/"
    for i in range (1,100):
        filename=path+str(i)+".txt"
        with open(filename, 'r') as file:
            lines = file.readlines()
            s2 = lines[0]
            length = len(s2)
            lines = lines[2:]
            score = np.zeros(shape=(len(lines)))
            for i in range(0, len(lines)):
                score[i] = editDistance(lines[i].strip(),s2)

            guess = score.argsort()[-k:]
            guess_string = ""
            for ind in guess:
                guess_string = guess_string + str(ind+1) + " "
            print(os.path.basename(filename) + " " + guess_string)


if __name__=="__main__":
    main(sys.argv[1:])
