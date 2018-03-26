import sys,math

class LineOutOfRangeException(Exception):
    pass

def lossFunction(guess, solution):
    if(solution[0] > guess[1] or guess[0] > solution[1]):
        return math.tanh(guess[1]-guess[0]+1)
    else:
        correct_s = max(guess[0], solution[0])
        correct_e = min(guess[1], solution[1])
        missed_correct_lines = (solution[1]-solution[0])-(correct_e-correct_s)
        wrong_lines = 0
        if(correct_s < solution[0]):
            wrong_lines += solution[0]-correct_s
        if(correct_e > solution[1]):
            wrong_lines += solution[1]-correct_e
        return math.tanh(missed_correct_lines) + math.tanh(wrong_lines)

def main():
    k = 0 # Maximum number of solutions received

    path_files = "../Files_Hunk/"
    path_solutions = "../Solutions_Hunk/"

    total = 0
    correct = 0
    loss = 0
    for args in sys.stdin:
        inputs = args.split()
        filename = inputs[0]
        answers = inputs[1:]
        answers = [int(answer) for answer in answers]
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
                if(answer < 1 or answer > code_file_length):
                    raise LineOutOfRangeException("Line number out of range. Expected: 1<={line}<=" + str(code_file_length) + ", found: " + str(answer))

            solution_line = solution_file.readline().split()
            solution_line = [int(i) for i in solution_line]
            # Use minimum loss among all answers to calculate loss
            min_loss = float('Inf')
            for i in range(0, len(answers)/2):
                if(lossFunction(answers[2*i:2*(i+1)], solution_line) < min_loss):
                    min_loss = lossFunction(answers[2*i:2*(i+1)], solution_line)
                if(answers[2*i] == solution_line[0] and answers[2*i+1] == solution_line[1]):
                    correct+=1
                    break
            total+=1
            loss+=min_loss

            code_file.close()
            solution_file.close()
        except ValueError:
            print(line + " should be integer")
            raise
        except IOError:
            print(filename + " does not exist!")
            raise
    print("Total files: " + str(total))
    print("Cumulative range error: " + str(loss))
    print("Top " + str(k) + " accuracy: " + str(correct/(total*1.0)))

if __name__=="__main__":
    main()
