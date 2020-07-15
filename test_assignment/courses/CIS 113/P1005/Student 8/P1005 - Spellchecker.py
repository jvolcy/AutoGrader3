#P1005/P1405 - Spellchecker
#This program that prompts a user for a sentence then spell-checks the
#sentence. The program should output every misspelled word in the
#sentence.Assume that any word not in the words.txt file is a misspelled word.

def main():
    #create an empty list
    words = []
    
    #open words.txt file
    wordFile=open('words.txt','r')
    
    #read each word and append it to the list
    for word in wordFile:
        words.append(word.strip())

    #close the file
    wordFile.close()
    
    #ask the user for a sentence
    sentence = input('Enter a sentence: ')

    #split every word in the sentence and turn into a list
    newSent = sentence.split()
    
    #spell check the sentence from words.txt
    for y in newSent:
        #output every misspelled sord in the sentence
        if y not in words:                 
            print(y)


main()
