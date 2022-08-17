import array
import random
import time as tm

import numpy as np

import tsp_plotter

"""
PART 0
DEAP dependencies
"""
from deap import base, creator
from deap import tools
from deap import algorithms

"""
PART 1
read TSP instance
"""
import TSPLIBReader

input_file = "TSPLIB/dantzig42.tsp"
D, I = TSPLIBReader.read_TSPLIB_instance(input_file)
n = len(D)  # number of nodes in the graph


# fitness function definition for the TSP
def fitness_function(ind):
    distance = 0
    for i in range(n - 1):
        distance += D[ind[i]][ind[i + 1]]
    
    # add returning cost
    distance += D[ind[-1]][ind[0]]
    return distance,


"""
PART 2
SETUP DEAP framework parameters
"""
pop_size = 200  # population size
n_gen = 200  # number of generations
pm = 1.0 / n  # mutation probability
pcx = 1  # recombination probability
k = 3  # tournament selection

"""
weight:
    +1.0 for maximization
    -1.0 for minimization
"""
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)
toolbox = base.Toolbox()

# representation of individuals
toolbox.register("permutation", random.sample, range(n), n)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.permutation)

# representation of population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# set fitness function
toolbox.register("evaluate", fitness_function)

# set recombination operator
toolbox.register("mate", tools.cxPartialyMatched)

# set mutation operator
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=pm)

# set selection operator
toolbox.register("select", tools.selTournament, tournsize=k)

"""
PART 3
SETUP and RUN simple Genetic Algorithm
"""
seed = 0
random.seed(seed)

pop = toolbox.population(n=pop_size)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
# stats.register("Avg", np.mean)
# stats.register("Std", np.std)
stats.register("Min", np.min)
stats.register("Max", np.max)

# run Genetic Algorithm
st = tm.time()
pop, log = algorithms.eaSimple(pop, toolbox, cxpb=pcx, mutpb=pm, ngen=n_gen, stats=stats,
                               halloffame=hof, verbose=True)
# get the running time
elapsed_time = tm.time() - st
print('Execution time:', elapsed_time, 'seconds')

"""
PART 4
PLOT SOLUTION AND CONVERGENCE
(only for EUC2D instances)
"""
# get best individual ever seen
best_ind = hof.items.pop(0)

# plot solution
tsp_plotter.print_graph([tuple(l) for l in I.DISPLAY_DATA_SECTION],
                        list(best_ind), best_ind.fitness.values[0])

# plot convergence
tsp_plotter.print_convergence([log[i]["Min"] for i in range(n_gen)], "fitness")
