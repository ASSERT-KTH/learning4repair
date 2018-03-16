import sys,math

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    return math.tanh(abs(solution-guess))

def main():
    k = 0 # Maximum number of solutions received

    path_files = "../../Files_Hunk/Replaced/"
    path_solutions = "../../Solutions_Hunk/Replaced/"

    total = 0
    correct = 0
    #loss = 0
    for args in sys.stdin:
        inputs = args.split()
        filename = inputs[0]
        answers = inputs[1:]
        if(len(answers)/2 > k):
            k = len(answers)/2
        try:
            code_file = open(path_files+filename, "r")
            solution_file = open(path_solutions+filename, "r")

            file_lines = code_file.readlines()
            for i in range(0,len(file_lines)):
                if(file_lines[i].startswith("@@@")):
                    insert_end = i
                    break

            code_file_length = len(file_lines)-insert_end-1

            for answer in answers:
                if(int(answer) < 1 or int(answer) > code_file_length):
                    raise LineOutOfRangeException("Line number out of range. Expected: 1<={line}<=" + str(file_length) + ", found: " + line)

            solution_line = solution_file.readline().split()
            for i in range(0, len(answers)/2):
                if(int(answers[2*i]) == int(solution_line[0]) and int(answers[2*i+1]) == int(solution_line[1])):
                    correct+=1
                    break
            total+=1
            #loss+=lossFunction(int(line), int(solution_line))

            code_file.close()
            solution_file.close()
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
