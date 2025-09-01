#This is our Markov chain representation
import random

#define the graph in terms of vertices

class Vertex:
    def __init__(self, value): #value will be the word
        self.value = value
        self.adjacent = {} # nodes that hav an edge from this vertex
        self.neighbour = []
        self.neighbour_weights = []

    def add_edge_to(self, vertex, weight = 0):
        #adding an edge to the vertex we input the weight
        self.adjacent[vertex] = weight

    def increment_edge(self, vertex):
        #incrementing the weight of the edge
        #get() if a func that will matches any similiar keys in the dictionary 
        #and if there's none smiliarity, it will return the second parameter value which is 0 in this case
        self.adjacent[vertex] = self.adjacent.get(vertex, 0) + 1

#Now, that we have our Vertex representation , we put this together in a graph

    def get_probability_map(self):
        for (vertex, weight) in self.adjacent.items():
            self.neighbour.append(vertex)
            self.neighbour_weights.append(weight)

    def next_word(self):
        #randomly select next word based on their weights!
        #use random.choice()
        #since random func will return a list, we need to initalize it to return the first list which is index 0
        return random.choices(self.neighbour, self.neighbour_weights)[0]


class Graph:
    def __init__(self): #there's none init parameter due to Vertex(class) mapping
        self.vertices = {}

    def get_vertex_values(self):
        #what are the values of all the vertices?
        #in other words, return all POSSIBLE WORDS
        return set(self.vertices.keys())

    def add_vertex(self, value):
        #adding the vertex based on the vertex mapping
        self.vertices[value] = Vertex(value)
    
    def get_vertex(self, value):
        if value not in self.vertices: #what if the value isn't in the graph?
            self.add_vertex(value)
        return self.vertices[value] #get the Vertex object

    def get_next_word(self, current_vertex):
        return self.vertices[current_vertex.value].next_word()

    def generate_probability_mappings(self):
        for vertex in self.vertices.values():
            vertex.get_probability_map()

    