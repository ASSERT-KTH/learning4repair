import sys

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    return abs(solution-guess)

def main():
    path_solutions = "../../Solutions/Added/"
    path_files = "../../Files/Added/"
    loss = 0;
    for line in sys.stdin:
        [filename, line] = line.split()
        try:
            file = open(path_files+filename, "r")
            solution = open(path_solutions+filename, "r")

            file_length = len(file.readlines())-2
            if(int(line) < 0 or int(line) > file_length+1):
                raise LineOutOfRangeException("Line number out of range. Expected: 0<={line}<=" + str(file_length) + ", found: " + line)

            loss+=lossFunction(int(line), int(solution.readline()))

            file.close()
            solution.close()
        except ValueError:
            print(line + " should be integer")
            raise
        except IOError:
            print(filename + " does not exist!")
            raise
    print("Loss: " + str(loss))

if __name__=="__main__":
    main()
