import sys,math

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    return math.tanh(abs(solution-guess))

def main():
    k = 0 # Maximum number of solutions received

    path_solutions = "/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition/Solutions_Hunk/Replaced/"
    path_files = "/Users/zimin/Desktop/KTH/Master-Thesis/one-liner-competition/Files_Hunk/Replaced/"

    total = 0
    correct = 0
    #loss = 0
    for line in sys.stdin:
        input = line.split()
        filename = input[0]
        lines = input[1:]
        if(len(lines)/2 > k):
            k = len(lines)/2
        try:
            file = open(path_files+filename, "r")
            solution = open(path_solutions+filename, "r")

            file_lines = file.readlines()
            for i in range(0,len(file_lines)):
                if(file_lines[i].startswith("@@@")):
                    insert_end = i
                    break

            file_length = len(file_lines)-insert_end-1

            for line in lines:
                if(int(line) < 1 or int(line) > file_length):
                    raise LineOutOfRangeException("Line number out of range. Expected: 1<={line}<=" + str(file_length) + ", found: " + line)

            solution_line = solution.readline().split()
            for i in range(0, len(lines)/2):
                if(int(lines[2*i]) == int(solution_line[0]) and int(lines[2*i+1]) == int(solution_line[1])):
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
    main()
