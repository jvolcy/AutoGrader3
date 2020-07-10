#Write a program that prompts a user for a sentence then spell-checks
#the sentence.  The program should output every misspelled word in the
#sentence.  Assume that any word not in the words.txt file is a misspelled
#word.

#Create an empty list
words=[]

#Open the word.txt file
wordFile = open('words.txt','r')
#Read each word and add it to our list
for word in wordFile:
    words.append(word.strip())
#Close the file
wordFile.close()

#Ask user to enter a sentence
#split the user's sentence into a list
#assuming the words are that arent in the list are misspelled
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Have user input a sentence
sentence = input('Please enter a sentence: ')

#Split the sentence
separatedSentence=sentence.split()

#Make a loop to determine if words inputed are in the dictionary file
for word in separatedSentence:
    #Print the words that are spelled correctly
    if word in words:
        print('It is spelled correctly!'
    #print the incorrect word
    else:
        print(word)
