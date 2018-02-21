import os,glob,random

def randomLineOfFile(file):
    total = len(file.readlines())
    return random.randint(1,total+1)

def guess():
    path = "../../Files/Removed"
    for filename in glob.glob(os.path.join(path, "*.txt")):
        with open(filename, 'r') as file:
            print(os.path.basename(filename) + " " + str(randomLineOfFile(file)))

def main():
    guess()

if __name__=="__main__":
    main()
