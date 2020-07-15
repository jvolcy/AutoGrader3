#this is my program from spellchecker p1005

#call main function
def main():
    #create empty list for words
    words = []
    
    #open word list
    wordFile = open('words.txt', 'r')
    #read each word
    for word in wordFile:
        #store each word in the list
        strippedWord = word.rstrip()
        words.append(strippedWord)
        
    #close word file
    wordFile.close()
    
    #get sentence from user
    sentence = input('Enter a sentence: ')

    #convert a string containing spaces into a list of words
    sentenceList = sentence.split()

    #go through the sentence list
    for word in sentenceList:
        #check to see if the words in the sentence are in the words.txt file
        if word in words:
            #skip word if it is spelled correctly
            pass
        else:
            #if word is spelled incorrectly print out the word
            print(word)

   

main()
