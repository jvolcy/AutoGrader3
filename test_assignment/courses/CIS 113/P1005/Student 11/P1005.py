#P1005 - Spellchecker


def main():
    #create a list for the words from the file
    wordList = []
    #open the list
    wordFile = open('words.txt', 'r')
    #for every word in the list
    for word in wordFile:
        #strip the word
        strippedWord = word.rstrip()
        #add word to the end of the list
        wordList.append(strippedWord)
        #close the file
    wordFile.close()
    #user inputs sentence
    userInput = input('Please enter a sentence: ')
    #convert input into a list
    inputList = userInput.split()
    #for every word in the input list 
    for word in inputList:
        #if word is not in the words.txt list
        if word not in wordList:
            #print the word
            print('The incorrect word is:%s' % (word))
        #otherwise do nothing
        else:
            pass
main()

    
        
