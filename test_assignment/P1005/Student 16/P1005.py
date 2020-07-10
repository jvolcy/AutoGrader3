#Spell Checker


#function will print words misspelled in the sentence
def spellCheck(sentence):
    #will put user input into a list by spaces
    sentList = sentence.split()

    #open the file w/ the dictionary
    inputFile = open("words.txt","r")
    fileList = []
    #put items in file to a list to be able to check against sentList
    for word in inputFile:
        wordStripped = word.rstrip()
        fileList.append(wordStripped)
    inputFile.close()
    

     # will check if each word in sentList if not will print
    for elem in sentList:
        if elem not in fileList:
            print(elem)
    print()
    print("Above are the misspelled word(s):")

    

def main():
    #user input for function
    userSent = input("Enter a sentence: ")
    print()
    spellCheck(userSent)

#will run everything together
main()
