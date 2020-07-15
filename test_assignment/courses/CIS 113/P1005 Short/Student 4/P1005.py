#P1005 - Spellchecker

#create a new function that runs the sentence program and takes the user input
def splitter(x):
    #create an empty list
    sentence = []
    #open the file
    wordFile = open('words.txt', 'r')
    #split the user input
    splitter = x.split()
    #create a loop that reads each word in the file
    for word in wordFile:
        #strip each word of the new line character
        stripper = word.rstrip()
        #append each word to empty list
        sentence.append(stripper)
    #close the file
    wordFile.close()
    #create a loop that reads every word in the user input
    for users in splitter:
        #create a conditional to compare user input to list
        if users not in sentence:
            #return words that meet conditional
            return users
#create a main function            
def main():
    #take user input
    user = input('Write a sentence:')
    #pass argument to other function
    x = splitter(user)
    #print value returned from other function by calling the function
    print (splitter(x))
    #print result statements
    print ('This word is spelled incorrectly')
#call main
main()
