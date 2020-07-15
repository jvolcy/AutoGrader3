# 11/17/19
# P1005 - Spellchecker


# creating a main function
def main ():
    # creating a list variable
    VocabList = []
    # oeping the dictionary file
    dictionary = open('words.txt', 'r')

    # asking the user for a sentense
    UserSentence = input('Please write out a sentence here: ')
    # dividing every word in the sentence into individual elements in list
    user_strip = UserSentence.split()

    # for loop that takes away the '\n' from every word in the dictionary
    for Totalwrds in dictionary:
        # this is where the '\n' is being taken away
        dict_strip = Totalwrds.rstrip()
        # converting the 'new' words to the vacob list 
        VocabList.append(dict_strip)

    # for loop to identify whether the words are in the dictionary or spelled correctly
    for wrds in user_strip:
        # if statement to see if its in the vacab list
        if wrds in VocabList:
            # if it is ignore it
            pass
        # if not print the wrong word
        else:
            print('You spelled', wrds, 'wrong')


#calling main
main()
    
