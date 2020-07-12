#P1005
#Spellchecker



def main():
    #open file
    inputFile = open('words.txt', 'r')
    #get user input for a sentence
    userInput = input('Enter a sentence: ')
    #create list from input
    userSplit = userInput.split()
    #make list for words
    wordList = []
    #read through the file
    for word in inputFile:
        #strip the \n character off of the words
        wordStripped = word.rstrip()
        #add the words to a new file
        wordList.append(wordStripped)
    #read user input
    for words in userSplit:
        #if the word is in the list then dont do anything
        if words in wordList:
            words = ''
        #print words that are not in the list
        else:
            print(words, 'is spelled incorrectly.')

main()
