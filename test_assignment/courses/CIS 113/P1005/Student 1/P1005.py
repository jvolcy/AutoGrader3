#P1005- Spellchecker

def main():
    #create and empty list for the words in the dictionary
    wordsList = []
    #open the words text file
    dictionary = open('words.txt','r')

    #prompt the user for a sentence to spellcheck
    userInput = input('Write a sentence that you want to spellcheck: ')
    
    #make each word in the user's sentence (string) an item in a list
    splitInput = userInput.split()

    #put each word in the dictionary into a list
    for word in dictionary:
        #strip the end character from each word
        strippedWords = word.rstrip()
        #add the stripped word into the words list
        wordsList.append(strippedWords)

    #check to see if each word in the user's list is also in the dictionary
    for word in splitInput:
        if word in wordsList:
            #ignore words that are spelled correctly
            pass
        else:
            #identify and output every misspelled word in the sentence
            print(word,'is spelled incorrectly.')

main()
