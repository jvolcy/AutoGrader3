#P1005 - Spellchecker

#Define main function
def main():
    #Open, read and convert the word file to a list
    wordsFile = open('words.txt','r',).read().split()
    #Ask the user to type a sentence and assign it to the varibale userSentence
    userSentence = input('Enter a sentence: ')
    #Use the split method to convert the sentence to a list and assign it to the
    #variable userSen_List
    userSen_List = userSentence.split()

    print(userSen_List)
    #Go through each element in the list and check if it matches any word in the
    #word file
    for i in userSen_List:
       for word in wordsFile:
           #If it does not match any word in the word file print the word
            if i != word in wordsFile:
                print('misspelled word(s): ' , i)
                break
        

main()

    
