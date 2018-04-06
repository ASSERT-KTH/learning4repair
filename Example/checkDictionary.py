import pickle

def main():
    with open("Embedding_100000files_10000vol/dictionary.pickle" , "rb") as f:
        [count,dictionary,reverse_dictionary,vocabulary_size] = pickle.load(f)

    if("close" in dictionary):
        print("Yes")

    if("shutdown" in dictionary):
        print("Another yes")

if __name__=="__main__":
    main()
