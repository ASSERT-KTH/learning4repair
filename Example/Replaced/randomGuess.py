import os,glob,random

def randomLineOfFile(file):
    total = len(file.readlines())-2
    return random.randint(1,total)

def guess():
    path = "../../Files/Replaced"
    for filename in glob.glob(os.path.join(path, "*.txt")):
    #for i in range(1,100):
        #filename=path+"/"+str(i)+".txt"
        with open(filename, 'r') as file:
            print(os.path.basename(filename) + " " + str(randomLineOfFile(file)))

def main():
    guess()

if __name__=="__main__":
    main()
