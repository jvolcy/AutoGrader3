#P1005
####Write a program that prompts a user for a sentence then spell-checks the sentence.
#The program should output every misspelled word in the sentence.
##Assume that any word not in the words.txt file is a misspelled word.

# I, Im is not in list

def main():
    #open words file
    wordsFile = open('words.txt','r')
    # the user input
    userInput = input('Please enter a sentence: ')
#words list for the words file
    wordsList = []
    #split user Input into a list
    UserList = userInput.split()
    #strip the words in word file and make them into a list
    for words in wordsFile:
        strippedWords = words.rstrip()
        wordsList.append(strippedWords)
#for the words in user list
    for words in UserList:
        #if the word in userList is in words file list
        if words in wordsList:
            #set words = 0 to make it do nothing
            words = 0
            #if words is not in list print output
        else:
            print(words, ' is spelled incorrectly')
        
    wordsFile.close()
    
            
        
        
        








main()
    
