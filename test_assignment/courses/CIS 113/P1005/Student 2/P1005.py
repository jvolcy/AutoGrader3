#P1005/P1405- Spellchecker 
#This program checks if the entered sentence contains all words within
#the dictionary and is spelled correctly. 
#containcs actual 


def SentenceCheck():
    #create a list
    dictionary = []
    
    #open file and read it 
    dict_file = open('words.txt', 'r')
    
    #Prompt user to enter sentence
    user_sentence = input("Write a sentence, please: ")
    
    #make the user input a list of words 
    userinput_list = user_sentence.split()
    
    #print(check_input)

    for word in dict_file:
        #store/append each word in the file to a list 
        strippedWords = word.rstrip()
        dictionary.append(strippedWords)

    #go through the sentence entered by the user and check if it is in the
        #dictionary list
    for word in userinput_list:
        if word not in dictionary:
            print(word)
        else:
            pass
        


SentenceCheck() 
