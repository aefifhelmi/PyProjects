#Start here!
from cryptography.fernet import Fernet

def writekey():
  key = Fernet.generate_key()
  with open("key.key","wb") as key_file:
    key_file.write(key)

def load_key():
  file = open("key.key", "rb")
  key = file.read()
  file.close()
  return key

key = load_key() 
fer = Fernet(key)

def add(): #This function allow us to create a new file to store our username and password!
  name = input("Username: ")
  pwd = input("Password: ")

  with open("passwords.txt", "a") as f:
    f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")


def view(): #This function allow us to view our Username and Password proficiently!
  with open("passwords.txt", "r") as f:
    for line in f:
      data = line.readline()
      user , passw = data.split("|") #split() will allow us to delete irrelevant syntax and store the value in a list!
      print("Username: ", user, " | Password: ", fer.decrypt(passw.encode()).decode())

while True:
  mode = input("Would you like to add a new password or view teh existing ones (add, view)? , press q to quit").lower()

  if mode == "q":
    break

  if mode == "view":
    view()
  elif mode == "add":
    add()
  else:
    print("Invalid mode. ")
    continue

