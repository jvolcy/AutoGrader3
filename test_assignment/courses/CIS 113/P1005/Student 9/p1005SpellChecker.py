#p1005 Spell Checker

#write the words in the words file to a list

def main():
    #create list for words in the word file
    dictionaryWords =[]
    
    #create list for words that were spelled wrong
    incorrectlySpelledWords=[]
    
    #open the words file for reading
    wordFile = open('words.txt','r')

    #read each word
    for word in wordFile:
        #strip the newline character
        strippedWord = word.rstrip()

        #append each word in the file to the dictionary list
        dictionaryWords.append(strippedWord)
        
    #close words file
    wordFile.close()
   
   #have the user enter a sentence
    userinput =input('Enter a sentence: ')
    
    #convert sentence to list using split
    splitSentence = userinput.split()

    #go through each word in the userinput sentence
    for word in splitSentence:
    #if words in sentence are not in the dictionary,print the word
    #don't print anything if word is spelled right
        if word in dictionaryWords: 
            print('')
    #if word is spelled wrong add it to incorrectly spelled list
        else:
            incorrectlySpelledWords.append(word)
    print('The words that were spelled wrong are: ', incorrectlySpelledWords)
    
main()


