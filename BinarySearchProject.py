import random
import time


#Naive Search

def naive_search(l, target):  #By naive search, the programme will run each of the element in the list, and if there is none, "-1" will show up
    for i in range(len(l)): #we can do it by using for loops
        if target == l[i]:
            return i

    return -1

#Binary Search , it uses dive and conquer method!

def binary_search(l, target, low = None, high = None):

    if low is None:
        low = 0

    if high is None:
        high = len(l) - 1 #must substract by 1 to make it the right numbering for list, len(l) numbering always start from 1 not 0!

    if low > high:
        return -1 #Happens if the target is not on the list

    midpoint = (high + low) // 2 #2

    if target == l[midpoint]:
            return midpoint

    elif target > l[midpoint]:
            return binary_search(l, target, midpoint + 1, high)

    else:
            return binary_search(l, target, low, midpoint - 1)

if __name__ == "__main__":

    l = [1,3,5,10,12] #Starting from the left of the list, the numbering is 0
    target = 10

    print(binary_search(l, target))
    print(naive_search(l, target))

    #Proven Part in Seconds, Which is Faster?

    lenght = 10000 #set the length of numbering to 10000
 
    sorted_list = set()
    while len(sorted_list) < lenght:
         sorted_list.add(random.randint(-3*lenght, 3*lenght)) #choosing a random number by using random module, from -30000 < 0 < 30000

    sorted_list = sorted(list(sorted_list)) # make "sorted_list" as a list and sorted! , if that make sense!

#Naive search timer
    start = time.time() #start counting

    for target in sorted_list:
        naive_search(sorted_list, target)

    end = time.time() #end counting
    print("Naive Search Time: ", (end - start)/lenght, "SECONDS") #must divide by lenght to know each of the naive search duration
#Binary search timer
    start = time.time()

    for target in sorted_list:
        binary_search(sorted_list, target)

    end = time.time()
    print("Binary Search Time: ",(end - start)/lenght, "SECONDS")




   








