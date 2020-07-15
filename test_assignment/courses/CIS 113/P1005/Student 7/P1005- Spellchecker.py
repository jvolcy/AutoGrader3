#P1005- Spellchecker

#Write a program that prompts a user for a sentence then spell-checks the
#sentence.
#The program should output every misspelled word in the sentence.
#Assume that any word not in the words.txt file is a misspelled word.

def main():
    #create an empty list 
    dictionary=[]
    
    #open words.txt
    wordFile= open('words.txt','r')
    
    #ask the user to input a sentence
    sentence=input('Enter a sentence: ')
    #use the split method to turn the sentence into a list
    checkList= sentence.split()
    
    #go through every word in the word file 
    for words in wordFile:
        #strip each word of the new line charater 
        strippedWords=words.rstrip()
        #add each stripped word to the list "dictionary"
        dictionary.append(strippedWords)

    #check that every word in checkList is also in the dictionary
    for word in checkList:
        #if it is not in the dictionary than print the mispelled word 
        if word not in dictionary:
            print('The misspelled word(s) are: ',word)
        else:
            pass
    
    #if the word is not in the list print it 
    #close words.txt

main()
