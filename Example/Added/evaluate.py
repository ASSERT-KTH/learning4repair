import sys

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    return abs(solution-guess)

def main():
    path_solutions = "../../Solutions/Added/"
    path_files = "../../Files/Added/"
    total = 0
    correct = 0
    loss = 0;
    for line in sys.stdin:
        [filename, line] = line.split()
        try:
            file = open(path_files+filename, "r")
            solution = open(path_solutions+filename, "r")

            file_length = len(file.readlines())-2
            if(int(line) < 0 or int(line) > file_length+1):
                raise LineOutOfRangeException("Line number out of range. Expected: 0<={line}<=" + str(file_length) + ", found: " + line)

            solution_line = solution.readline()
            if(int(solution_line) == int(line)):
                correct+=1
            total+=1
            loss+=lossFunction(int(line), int(solution_line))

            file.close()
            solution.close()
        except ValueError:
            print(line + " should be integer")
            raise
        except IOError:
            print(filename + " does not exist!")
            raise
    print("Total files: " + str(total))
    print("Loss: " + str(loss))
    print("Accuracy: " + str(correct/(total*1.0)))

if __name__=="__main__":
    main()
