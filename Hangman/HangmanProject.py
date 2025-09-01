import random
from wordsforhangman import words
import string
import time

def Timer(number, name):
    if (number==0):
        print("YOU LOSE", name,"!")
    
    elif (number==5):
        print("IM SORRY", name, "BUT....")
        return Timer(number-1, name)

    else:
        time.sleep(1)
        print(number)
        return Timer(number-1, name)

def get_valid_word(words): #To exclude words that contains dash or space!
    word = random.choice(words) 
    while "-" and " " in words: #Excluding process
        random.choice(words)

    return word.upper()

def hangman():
    word = get_valid_word(words) #word that been chosen randomly and excluded!
    word_letters = set(word) #Letters in word
    alphabet = set(string.ascii_uppercase) #an alphabet function from A-Z in uppercase
    used_letters = set() #used letter storagess
    lives = 6

        #A condition must started out to make the game replayable!
    while len(word_letters) > 0 and lives > 0:
        #if the length of words == 0, the while loop will break
        #We need two things to tell the user  output, 1) What letters that they have already used, 2)What current words left is?
        print("You have ", lives, "lives left and You Have Used These Letters: ", " ".join(used_letters)) #1

        print(" ")

        #join function is used for space string " ", ex: " ".join(["b", "c"]) ---> "b c"

        word_list = [letter if letter in used_letters else "-" for letter in word] #2), what does this list actually mean is that every singgle letter user have guessed correctly is shown and letters that haven't been guessed is visble by dash "-"
        print("Current Word: ", " ".join(word_list)) 

        print(" ")

        user_letter = input("Guess A Letter: ").upper()
        print(" ")
        if user_letter in alphabet - used_letters: #Add a storage in used_letter
            used_letters.add(user_letter)

            if user_letter in word_letters: #If the letter guessed correctly, the size of user letter will be deduced!
             word_letters.remove(user_letter)

            else:
                lives = lives - 1
                print("Incorrect Letter")

        elif user_letter in used_letters:
             print('You already used that character, Please Try Again!')

        else:
             print("Invalid Character, Please Try Again!")

    if lives == 0:
        Timer(5, input("Enter Your name: "))
        print(" ")
        print('The word was', word, "!")
    else:
        print("You Guessed The Word ", word, "!!" ) 

hangman()



    



