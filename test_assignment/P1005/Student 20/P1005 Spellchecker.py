#create an empty list
words = []

#open the words.txt file
inputFile = open('words.txt', 'r')

#read in each line from words.txt and appended it to the words list
for word in inputFile:
    words.append(word.strip())
    
#close the input file
inputFile.close()



#ask user for a sentence
user_sentence = input("Plase enter a sentence: ")

#split the user's sentence into a list
split_sentence = user_sentence.split()

#check each word in the user's sentence against the words.txt file
#assume words not in the words list are misspelled
for item in split_sentence:
    if item not in words:
        
        #if the word is mispelled, print it
        print(item)

