#Translating every vowels in every phrase into U or u
#I called this bahasa Kuntul

def translate(phrase):
    translation = ""  #Use empty string
    for letter in phrase:
        if letter.lower() in "aeiou":     #Lowercase Vowels
            if letter.isupper():
                translation = translation + "U"     #Use Uppercase Condition First!

            else:
                translation = translation + "u"

        elif letter.lower() in "bcdfBCDF":   #Addition simple translator
            translation = translation + "4"

        else:
            translation  = translation + letter

    return translation  #Must return!!

print(translate(input("Enter Your Phrase: "))) 




