import re,math,os,glob,random,getopt,sys,operator
import numpy as np

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

    path = "../../Files_Hunk/Replaced"
    for filename in glob.glob(os.path.join(path, "*.txt")):
    #for a in range(1, 101):
        #filename = path+"/"+str(a)+".txt"
        with open(filename, 'r') as file:
            lines = file.readlines()

            for i in range(0,len(lines)):
                if(lines[i].startswith("@@@")):
                    insert_end = i
                    break

            insert = lines[:insert_end]
            for i in range(0,len(insert)):
                insert[i] = filter(None,re.split("[,.();_\t\n ]",insert[i]))

            lines = lines[insert_end+1:]
            for i in range(0,len(lines)):
                lines[i] = filter(None,re.split("[,.();_\t\n ]", lines[i]))

            # Assume tf is 1 in the inserted lines
            weight_insert = []
            for line in insert:
                for token in line:
                    freq = 0
                    for i in range(0,len(lines)):
                        if token in lines[i]:
                            freq+=1
                    if(freq == 0):
                        weight_insert.append(1)
                    else:
                        weight_insert.append(math.log(len(lines)/(freq*1.0)))
            weight_insert = normalize(weight_insert)

            tfidf_vectors = np.zeros(shape=(len(lines), len(weight_insert)))
            for i in range(0, len(lines)):
                count = 0
                for m in range(0, len(insert)):
                    for n in range(0, len(insert[m])):
                        if(insert[m][n] in lines[i]):
                            tf=lines[i].count(insert[m][n])
                            idf=weight_insert[count]
                            tfidf_vectors[i][count] = tf*idf
                            count+=1
                        else:
                            tfidf_vectors[i][count] = 0
                            count+=1

            # Only looking for hunk with similar size
            max_diff = len(insert)
            score = {}
            for i in range(0, len(lines)+1):
                for j in range(i+1, len(lines)+1):
                    if(j-i > max_diff):
                        break
                    vec = np.zeros(shape=(len(weight_insert)))
                    for n in range(i,j):
                        vec = vec + tfidf_vectors[i]
                    vec = normalize(vec)
                    score[(i+1,j)] = cosine_sim(weight_insert, vec)

            score_cmp = lambda ((s1, e1), v1), ((s2,e2), v2):cmp((v1, e2-s2), (v2, e1-s1))
            sorted_score = sorted(score.items(), cmp=score_cmp, reverse=True)

            guess_string = ""
            for i in range(0,min(k, len(sorted_score))):
                guess_string = guess_string + str(sorted_score[i][0][0]) + " " + str(sorted_score[i][0][1]) + " "

            print(os.path.basename(filename) + " " + guess_string)
            '''
            guess = score.argsort()[-k:][::-1]
            guess_string = ""
            for ind in guess:
                guess_string = guess_string + str(ind+1) + " "

            print(os.path.basename(filename) + " " + guess_string)
            '''


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
