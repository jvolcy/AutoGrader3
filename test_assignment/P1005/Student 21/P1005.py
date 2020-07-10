#P1005 -Spellchecker

def main():
    #Create an empty list
    wordList = []
    #Open the words file
    wordFile = open('words.txt', 'r')
    #Ask the user to enter a sentence
    user_input = input("Enter a sentence: ")
    #Split the user's input into a list
    a = user_input.split()
    #Read each word in the file
    for word in wordFile:
        #Strip the newline character
        strippedWord = word.rstrip('\n')
        #Store each word in a list
        wordList.append(strippedWord)
    #Close the wordFile 
    wordFile.close()
    #Read each word in the user's input
    for word in a:
        #If the word from the user's input
        #Does not exist in the wordList
        if word not in wordList:
            #Print the misspelled word
            print('The misspelled word(s) is', word)
        #Otherwise do nothing 
        else:
            pass
#Call to the main function 
main()
