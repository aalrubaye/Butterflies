__author__ = 'Abdul Rubaye'
import networkx as nx
import random

graph = nx.Graph()
nodes = []
next_color = 'red'
next_index = 0
L = []
bipartite = None

# number_of_betterflies = random.randint(3,10)
number_of_betterflies = 6

# number_of_species = random.randint(2,5)
number_of_species = 2


# return a random number indicating different specimens
def generate_random_specimens():
    butterflies = []
    for i in range (0, number_of_betterflies):
        butterflies.append(i)
    return butterflies


# return a random array correspondent to the spcimens' different species
def generate_random_species(specimens_count):
    specimens_type = []
    for i in range (0, specimens_count):
        specimens_type.append('Species-Type-'+str(random.randint(0, number_of_species-1)))
    return specimens_type


# The function below generates a network G=(V,E)
# Creates a node for each butterfly
# Creates an additional node for each "same" judgement
# For each "same" judgement, connect the responding nodes (i) and (j) to the additional node
# For each "different" judgement, connect the responding nodes (i) and (j)
def generate_network_of_butterflies_judgement(butterflies, butterflies_types):
    global graph, nodes, visited
    for i in range (0, len(butterflies)):
        graph.add_node('Butterfly-'+str(i), color='none', visited=False)
        nodes.append('Butterfly-'+str(i))
    print 'Specimens of Butterflies = '+ str(nodes)

    for i in range (0, len(butterflies)):
        for j in range (i+1, len(butterflies)):
            if butterflies_types[butterflies[i]] == butterflies_types[butterflies[j]]:
                new_node_label = 'Same-Type-B'+str(i)+'-B'+str(j)
                nodes.append(new_node_label)
                graph.add_node(new_node_label, color='none', visited=False)
                graph.add_edge('Butterfly-'+str(i), new_node_label)
                graph.add_edge('Butterfly-'+str(j), new_node_label)

            else:
                graph.add_edge('Butterfly-'+str(i), 'Butterfly-'+str(j))



def validate_partiteness():
    global L
    current_node = nodes[0]
    graph.nodes[current_node]['color'] = next_color
    graph.nodes[current_node]['visited'] = True
    L.append(nodes[0])
    check_neighbors(current_node)




def check_neighbors(current_node):
    global next_color
    global next_index, L
    global bipartite

    if graph.nodes[current_node]['color'] == 'none':
        graph.nodes[current_node]['color'] = next_color

    if not graph.nodes[current_node]['visited']:
        graph.nodes[current_node]['visited'] = True

    neighbors = graph[current_node].keys()


    if graph.nodes[current_node]['color'] == 'red':
        next_color = 'blue'
    else:
        next_color = 'red'


    for i in range (0, len(neighbors)):
        if graph.nodes[neighbors[i]]['color'] == 'none':
            graph.nodes[neighbors[i]]['color'] = next_color
            graph.nodes[neighbors[i]]['visited'] = True
            L.append(neighbors[i])
        elif graph.nodes[neighbors[i]]['color'] == graph.nodes[current_node]['color']:
            bipartite = False

    next_index += 1
    if (next_index == len(nodes)):
        if bipartite == None:
            bipartite = True
    else:
        check_neighbors(L[next_index])


# The main function
if __name__ == "__main__":
    butterflies = generate_random_specimens()
    butterflies_types = generate_random_species(len(butterflies))

    generate_network_of_butterflies_judgement(butterflies, butterflies_types)

    print 'Species Type for each butterfly = '+str(butterflies_types)
    print ('-'*300)
    print 'The set of Nodes (V) ='+ str(graph.nodes())
    print 'The set of Edges (E) ='+ str(graph.edges())
    print ('-'*300)

    validate_partiteness()
    print
    print
    print ('-'*300)
    if bipartite:
        print "Result => The judgment was consistent (The network is Bipartite)"
    else:
        print "Result => The judgment was not consistent (The network is Not Bipartite)"
    print ('-'*300)
    nx.write_graphml(graph, "butterfliesGraph.graphml")
