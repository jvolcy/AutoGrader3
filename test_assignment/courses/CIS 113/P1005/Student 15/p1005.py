#spelchecker
#p1005


#then spell-checks the sentence.
#The program should output every misspelled word in the sentence.
#Assume that any word not in the words.txt file is a misspelled word.

def main():
    #Create a new list
    dictionary =[]
    #open the file and read it
    myFile = myFile = open("words.txt","r")
    #Write a program that prompts a user for a sentence
    sentence = input("Enter a string of words to create a sentence:")
    #make the sentence break from word to word
    split = sentence.split()
    print(split)

    for word in myFile:
        strip = word.rstrip()
        dictionary.append(strip)

    for word in sentence:
        if word not in dictionary:
            print('mispelled',word)
    else:
        pass
        
#call main
main()
