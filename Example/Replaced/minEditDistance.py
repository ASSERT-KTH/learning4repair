import edit_distance,math,os,glob

def editDistance(s1,s2):
    return edit_distance.SequenceMatcher(a=s1, b=s2).distance()

def main():
    path = "../../Files/Replaced/"
    for i in range (1,100):
        filename=path+str(i)+".txt"
        with open(filename, 'r') as file:
            lines = file.readlines()
            s2 = lines[0]
            length = len(s2)
            minEdit = float("inf")
            minEditLine = 0
            for i in range(2, len(lines)):
                if(len(lines[i].strip()) > minEdit+length):
                    continue
                distance = editDistance(lines[i].strip(),s2)
                if(distance < minEdit):
                    minEdit = distance
                    minEditLine = i-1
            print(os.path.basename(filename) + " " + str(minEditLine))


if __name__=="__main__":
    main()
