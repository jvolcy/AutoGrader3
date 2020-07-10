#P1005 -spellchecker

def SentanceCheck():
    #initialize a list
    dictionary= []

    #open file and read it
    word_file= open('words.txt', 'r')

    #prompt the user to enter a sentance
    user_sentance= input('Write a sentance: ')

    #make the user input into a list
    user_list= user_sentance.split()


    for word in word_file:
        #store/appened each word in the file to a list
        strippedwords= word.rstrip()
        dictionary.append(strippedwords)

        #go through the sentance entered by the user and check if it is in the
        #word.txt file
    for word in user_list:
        if word not in dictionary:
            print(word)
        else:
            pass

SentanceCheck()
