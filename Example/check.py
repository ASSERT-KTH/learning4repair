import sys

def main(argv):
    filename1 = argv[0]
    filename2 = argv[1]
    file1 = open(filename1, "r")
    file2 = open(filename2, "r")

    lines1 = file1.readlines()
    lines2 = file2.readlines()
    file1.close()
    file2.close()

    lines1 = [line.split() for line in lines1]
    lines2 = [line.split() for line in lines2]

    count = 0
    print(filename1 + " predicted wrong but not " + filename2)
    for line1 in lines1:
        exist = False
        for line2 in lines2:
            if(line1[0] == line2[0]):
                exist = True
                break
        if(not exist):
            #print(line1)
            count+=1
    print("Count: " + str(count))

    count = 0
    print(filename2 + " predicted wrong but not " + filename1)
    for line2 in lines2:
        exist = False
        for line1 in lines1:
            if(line2[0] == line1[0]):
                exist = True
                break
        if(not exist):
            #print(line2)
            count+=1
    print("Count: " + str(count))

    print("Both predicted wrong:")
    for line1 in lines1:
        for line2 in lines2:
            if(line1[0] == line2[0]):
                print(line1[0])
                break

if __name__=="__main__":
    main(sys.argv[1:])
