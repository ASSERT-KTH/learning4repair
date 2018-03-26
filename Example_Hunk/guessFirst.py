import os
import glob
import sys

def main():
    path_files = "../Files_Hunk"
    for filename in glob.glob(os.path.join(path_files, "*.txt")):
        with open(filename, 'r') as file:
            lines = file.readlines()

            for i in range(0,len(lines)):
                if(lines[i].startswith("@@@")):
                    insert_end = i
                    break

            insert = lines[:insert_end]
            insert_length = len(insert)

            lines = lines[insert_end+1:]
            program_length = len(lines)

            print(os.path.basename(filename) + " " + "1 " + str(min(insert_length,program_length)))


if __name__=="__main__":
    main()
