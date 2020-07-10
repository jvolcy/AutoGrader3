#P1005-Spellchecker

#create a main function 
def main():
    
    #create an empty list called 
    checkWords= []

    #ask the user to input a sentence
    sentence=input("Enter a sentence: ")

    #split the words in the sentence 
    sentenceSplit= sentence.split()

    #open words file 
    dictionary=open("words.txt","r")

    #make a for loop to go through each word in the dictionary
    for words in dictionary:
        AppendStrip=words.rstrip()
        checkWords.append(AppendStrip)

    #make a loop that check to see if the words in the sentence
        #are the same as the words in the dictionary 
    for words in sentenceSplit:
        if words in checkWords:
            pass
        #print the words that are not in the dictionary 
        else:
            print(words)
            
#call the main function            
main()

