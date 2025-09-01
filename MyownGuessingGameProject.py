
print("Who will win the Carabao Cup Tonight?: ")

guess_word = "Chelsea"
guess = ""
guess_count = 0
guess_limit = 3
out_of_guess = False

while guess != guess_word and not(out_of_guess):
    if guess_count < guess_limit:
        print("")
        guess = input("Enter your guess: ")
        if guess != guess_word:
            print("LIVERPOOL SUCKS BRO!")
            guess_count += 1

    else:
        out_of_guess = True

if out_of_guess:
    print("")
    print("WELL YOU GOTTA BRING A LOT OF TISSUE TONIGHT CAUSE CHELSEA WILL WIN YOU FUCKERS")

else:
    print("")
    print("YESSSSSS BROOOOOO THATS THE SPIRIT, WE ARE THE BEST CLUB IN THE WORLD!")

