#SPELLCHECKER


##EXAMPLE
##a = 'the quick brown fox jumps over the lazy dog'
##b = a.split()		#creates a list from the string of words
##print(b)

def main():
#create empty list for words
    listOfWords = []
#create empty list for the wrng spelled words
    wrongSpell= []
#opens the words file and reads it
    wordsFile = open('words.txt', 'r')
#read each word in the words
    for word in wordsFile:
    #strip the thw words
       strippedNameW = word.rstrip()
       #move the words into the new list
       listOfWords.append(strippedNameW)
    #close the file
    wordsFile.close()

#asks user to write a sentence
    userSent = input('Write a sentence:')
    #splits each word in the sentence
    words = userSent.split()
    
    for word in words:
        if word in listOfWords:
            print('You are all set')
        else:
            wrongSpell.append(word)
    #print the list of words from the sentence
            print(wrongSpell)
    
    

    

    
main()
