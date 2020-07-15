#P1005 - Spellchecker

#The main function is created
def main():

    #An empty lists is created
    dictionary = []
    
    #The "words.txt" file is opened and read
    wordsFile = open("words.txt", "r")

    #The user is prompted to enter a sentence
    sentence = input("Enter a sentence: ")
    
    #The string is split into a list called sentenceSplit
    sentenceSplit = sentence.split()

    #The list is printed
    print(sentenceSplit)

    #A for loop is created to go through each word in the file
    for words in wordsFile:
        
        #The white characters are stripped from each word and appended to
        #the list
        strip = words.rstrip()
        dictionary.append(strip)

    print("The misspelled words are: ")

    #A for loop is used to go through all the words in the list
    for word in sentenceSplit:

        #If the words in the list is not apart of the words file, that means
        #it is misspelled and prints      
        if word not in dictionary:
            print(word)
                  
        else:
            pass

    #The file is closed
    wordsFile.close()

#The main function is called   
main()
