import os,glob,random

def maximumError(file, solution):
    total = len(file.readlines())-2
    if(solution-1 > total-solution):
        return 1
    else:
        return total

def maximum():
    path = "../../Files/Replaced"
    for filename in glob.glob(os.path.join(path, "*.txt")):
        with open(filename, 'r') as file:
            with open(filename.replace("Files", "Solutions"), "r") as solution:
                print(os.path.basename(filename) + " " + str(maximumError(file,int(solution.readline()))))

def main():
    maximum()

if __name__=="__main__":
    main()
