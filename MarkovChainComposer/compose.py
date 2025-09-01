import string
import random
import re
import os

from graph import Graph, Vertex

#what we need to do?
def get_words_from_text(text_path):
    with open(text_path, 'r') as f:
        text = f.read() #makes the text file as a variable string

        text = re.sub(r'\[(.+)\]', " ", text) #this is a regex module, in this case, it means that subtitute (.+) with " " in the text file

        text = " ".join(text.split()) #this is saying turn whitespace into just space
        text = text.lower() #make everything lowercase to compare stuff

        #remove all the punctuations
        text = text.translate(str.maketrans("", "", string.punctuation))

    words = text.split()
    return words

def make_graph(words):
    g = Graph()
    previous_word = None

    #for each word
    for word in words:
        #check if that word is in the graph , and if not then add it
        word_vertex = g.get_vertex(word)


        #if there was a previous word, then add an edge if it does not already exist
        #in the graph, otherwise increment weight by 1
        if previous_word:
            previous_word.increment_edge(word_vertex)

        #set our word to the previous word and iterate!
        previous_word = word_vertex #to access and keep tracking the previous word

        #generate the probabilty mappings before composing
        #great place to do it before we return the graph object
    g.generate_probability_mappings()
    return g

def compose(g, words, length = 50): #g is graph!!
    composition = []
    word = g.get_vertex(random.choice(words))

    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition


def main(artist):
    # step 1: get words from text
    # words = get_words_from_text('pythonaefif.py3/PyProjects/MarkovChainComposer/texts/hp_sorcerer_stone.txt')

    #for song lyrics

    words = []
    for song_file in os.listdir(f"pythonaefif.py3/PyProjects/MarkovChainComposer/songs/{artist}"):
        song_words = get_words_from_text(f"pythonaefif.py3/PyProjects/MarkovChainComposer/songs/{artist}/{song_file}")
        words.extend(song_words)
    # step 2: make a graph using those words
    g = make_graph(words) #g is graph

    # step 3: get the next word for x number of words (defined by user)
    # step 4: show the user
    composition = compose(g, words, 100)
    # right now, the composition is in a list, use join() to turn it into a string
    return " ".join(composition) # it returns a string, where all the words are seperated by a space


if __name__ == "__main__":
    print(main("billie_eilish"))