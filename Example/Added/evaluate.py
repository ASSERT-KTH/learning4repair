import sys

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    return abs(solution-guess)

def main(argv):
    k = 0 # Maximum number of solutions received

    path_solutions = "/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition/Solutions/Added/"
    path_files = "/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition/Files/Added/"
    total = 0
    correct = 0
    #loss = 0
    for line in sys.stdin:
        input = line.split()
        filename = input[0]
        lines = input[1:]
        if(len(lines) > k):
            k = len(lines)
        try:
            file = open(path_files+filename, "r")
            solution = open(path_solutions+filename, "r")

            file_length = len(file.readlines())-2

            for line in lines:
                if(int(line) < 0 or int(line) > file_length):
                    raise LineOutOfRangeException("Line number out of range. Expected: 1<={line}<=" + str(file_length) + ", found: " + line)

            solution_line = solution.readline()
            for line in lines:
                if(int(solution_line) == int(line)):
                    correct+=1
                    break
            total+=1
            #loss+=lossFunction(int(line), int(solution_line))

            file.close()
            solution.close()
        except ValueError:
            print(line + " should be integer")
            raise
        except IOError:
            print(filename + " does not exist!")
            raise
    print("Total files: " + str(total))
    #print("Loss: " + str(loss))
    print("Top " + str(k) + " accuracy: " + str(correct/(total*1.0)))

if __name__=="__main__":
    main(sys.argv[1:])
