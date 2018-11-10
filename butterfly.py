import tqdm as tqdm

__author__ = 'Abdul Rubaye'
import networkx as nx
import random
import datetime
import matplotlib.pyplot as plt
import numpy as np

graph = nx.Graph()
nodes = []
colors = []
next_color = 'red'
next_index = 0
L = []
bipartite = None
test_cases_N = []
test_cases_S = []
expected_results = []
actual_results = []
time_array = []
N = []
S = []
positive_result = 'The judgment is consistent (Bipartite Network)'
negative_result = 'The judgment is not consistent (Not a Bipartite Network)'


# This function creates test cases for us
# First generates a list of n butterflies considered in each iteration
# Second generates a list of the type of butterflies in each iteration
# Calls the brute force algorithm to gets the expected results of the first 10 iterations
def create_test_cases_and_brute_force_correct_answers(n):
    global N,S

    N = list(range(1, n + 1))
    S.append(1)

    for i in range(1, n):
        S.append(random.randint(1, N[i]))

    for i in range (0, len(N)):
        butterfly = generate_random_specimens(N[i])
        butterfly_specie = generate_random_species(len(butterfly), S[i])

        test_cases_N.append(butterfly)
        test_cases_S.append(butterfly_specie)

    fw = open("Test_cases_and_correct_answers.txt","w")
    # brute-force to find the correct answers
    for i in range(0, 10):
        brute_force_algorithm(test_cases_N[i], test_cases_S[i])
        fw.write('Test Case '+str(i+1)+'\n')
        fw.write('\n')
        fw.write('Number of Butterflies = '+ str(N[i])+'\n')
        fw.write('Number of species = '+ str(S[i])+'\n')
        fw.write('Result (by Brute Force alg) = '+ str(expected_results[i])+'\n')
        fw.write(('='*100)+'\n')


# return a random number indicating different specimens
def generate_random_specimens(nb):
    butterflies = []
    for i in range(0, nb):
        butterflies.append(i)
    return butterflies


# return a random array correspondent to the spcimens' different species
def generate_random_species(specimens_count, num_of_species):
    specimens_type = []
    for i in range(0, specimens_count):
        specimens_type.append('S-' + str(random.randint(0, num_of_species - 1)))
    return specimens_type


# an algorithm to find the correct answer of a given set
def brute_force_algorithm(butterflies, butterflies_types):
    g = nx.Graph()
    v = []
    for i in range(0, len(butterflies)):
        g.add_node('B-' + str(i))
        v.append('B-' + str(i))
    for i in range(0, len(butterflies)):
        for j in range(i + 1, len(butterflies)):
            if butterflies_types[butterflies[i]] != butterflies_types[butterflies[j]]:
                g.add_edge('B-' + str(i), 'B-' + str(j))

    result = positive_result
    if has_odd_cycle(g, v):
        result = negative_result

    expected_results.append(result)


    g.clear()


# Checks whether a given network has an odd length cycle or not
def has_odd_cycle(g, v):
    for i in range (0, len(v)):
        c = nx.cycle_basis(g, v[i])
        for k in range (0, len(c)):
            if len(c[k]) % 2 != 0:
                # print 'Odd Cycle found'
                return True
    return False


# the implementation of my solution
def solution_implementation_and_validation():
    global time_array

    for i in tqdm.tqdm(range(len(test_cases_N))):
        generate_network_of_butterflies_judgement(test_cases_N[i], test_cases_S[i])

        # Gets the time of starting the operation
        start_time = datetime.datetime.now()

        if validate_partiteness():
            actual_results.append(positive_result)
            # print str(i+2) + positive_result
        else:
            actual_results.append(negative_result)
            # print str(i+2) + negative_result

        # Finds the elapsed time
        elapsed_time = datetime.datetime.now() - start_time

        time_array.append(elapsed_time.microseconds)


# The function below generates a network G=(V,E)
# Creates a node for each butterfly
# Creates an additional node for each "same" judgement
# For each "same" judgement, connect the responding nodes (i) and (j) to the additional node
# For each "different" judgement, connect the responding nodes (i) and (j)
def generate_network_of_butterflies_judgement(butterflies, butterflies_types):
    global graph, nodes
    for i in range(0, len(butterflies)):
        graph.add_node('B-' + str(i), color='none', visited=False)
        nodes.append('B-' + str(i))
        colors.append('none')

    for i in range(0, len(butterflies)):
        for j in range(i + 1, len(butterflies)):
            if butterflies_types[butterflies[i]] == butterflies_types[butterflies[j]]:
                new_node_label = 'B' + str(i) + '-B' + str(j)
                nodes.append(new_node_label)
                graph.add_node(new_node_label, color='none', visited=False)
                colors.append('none')
                graph.add_edge('B-' + str(i), new_node_label)
                graph.add_edge('B-' + str(j), new_node_label)

            else:
                graph.add_edge('B-' + str(i), 'B-' + str(j))


# validate the partiteness of a given network
def validate_partiteness():
    global L, next_index, next_color, bipartite
    current_node = nodes[0]
    graph.nodes[current_node]['color'] = next_color
    graph.nodes[current_node]['visited'] = True
    L.append(nodes[0])

    for i in range(0, len(nodes)):
        check_neighbors(L[next_index])

    graph.clear()
    del nodes[:]
    del L[:]
    del colors[:]
    next_color = 'red'
    next_index = 0
    actual_result = bipartite
    bipartite = None

    return actual_result


def check_neighbors(current_node):
    global next_color, next_index, L, bipartite

    if graph.nodes[current_node]['color'] == 'none':
        graph.nodes[current_node]['color'] = next_color

    if not graph.nodes[current_node]['visited']:
        graph.nodes[current_node]['visited'] = True

    neighbors = graph[current_node].keys()

    if graph.nodes[current_node]['color'] == 'red':
        next_color = 'blue'
    else:
        next_color = 'red'

    for i in range(0, len(neighbors)):
        if graph.nodes[neighbors[i]]['color'] == 'none':
            graph.nodes[neighbors[i]]['color'] = next_color
            graph.nodes[neighbors[i]]['visited'] = True
            L.append(neighbors[i])
        elif graph.nodes[neighbors[i]]['color'] == graph.nodes[current_node]['color']:
            bipartite = False

    next_index += 1
    if next_index == len(nodes):
        if bipartite is None:
            bipartite = True


def validate_correctness_of_test_cases():
    fw = open("Validating_test_cases_answers.txt","w")
    for i in range(0, 10):
        print
        print 'Test Case '+str(i+1)
        print
        print 'Number of Butterflies = ', N[i]
        print 'Number of species = ', S[i]
        print 'Result (by Brute Force alg) = ', expected_results[i]
        print 'Result (by my implementation) = ', actual_results[i]
        print ('='*100)

        fw.write('Test Case '+str(i+1)+'\n')
        fw.write('\n')
        fw.write('Number of Butterflies = '+ str(N[i])+'\n')
        fw.write('Number of species = '+ str(S[i])+'\n')
        fw.write('Result (by Brute Force alg) = '+ str(expected_results[i])+'\n')
        fw.write('Result (by my implementation) = '+ str(actual_results[i])+'\n')
        fw.write(('='*100)+'\n')


def plot_time_complexity(number_of_iterations):
    x = N
    y = time_array
    plt.plot(x, y, 'o', markersize=5, color='red')
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
    plt.title('Performance of the solution')
    plt.xlabel('n', fontsize=18)
    plt.ylabel('Millisecond', fontsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=16)
    plt.axis([0,len(N),0,time_array[number_of_iterations-2]])
    plt.show()


# The main function
if __name__ == "__main__":

    number_of_iterations = 400

    create_test_cases_and_brute_force_correct_answers(number_of_iterations)

    solution_implementation_and_validation()

    validate_correctness_of_test_cases()

    plot_time_complexity(number_of_iterations)






