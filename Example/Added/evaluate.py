import sys,math

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    return math.tanh(abs(solution-guess))

def main():
    k = 0 # Maximum number of solutions received

    path_solutions = "/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition/Solutions/Added/"
    path_files = "/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition/Files/Added/"
    total = 0
    correct = 0
    loss = 0
    for args in sys.stdin:
        inputs = args.split()
        filename = inputs[0]
        lines = inputs[1:]
        if(len(lines) > k):
            k = len(lines)
        try:
            file = open(path_files+filename, "r")
            solution = open(path_solutions+filename, "r")

            file_length = len(file.readlines())-2

            for line in lines:
                if(int(line) < 1 or int(line) > file_length):
                    raise LineOutOfRangeException("Line number out of range. Expected: 1<={line}<=" + str(file_length) + ", found: " + line)

            solution_line = solution.readline()
            for line in lines:
                min_loss = float('Inf')
                if(lossFunction(int(line), int(solution_line)) < min_loss):
                    min_loss = lossFunction(int(line), int(solution_line))
                if(int(solution_line) == int(line)):
                    correct+=1
                    break
            total+=1
            loss+=min_loss

            file.close()
            solution.close()
        except ValueError:
            print(line + " should be integer")
            raise
        except IOError:
            print(filename + " does not exist!")
            raise
    print("Total files: " + str(total))
    print("Loss: " + str(loss) + " (the lower, the better)")
    print("Top " + str(k) + " accuracy: " + str(correct/(total*1.0)) + " (the higher, the better)")

if __name__=="__main__":
    main()
