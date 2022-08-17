import array
import random
import time as tm

import numpy as np

import FAPProblem
import fap_plotter

"""
PART 0
DEAP dependencies
"""
from deap import base, creator
from deap import tools
from deap import algorithms

"""
PART 1
read FAP instance
"""
input_file = "FAP08/GSM2-272.ctr"
n, E = FAPProblem.read_problem(input_file)
F = 49


# fitness function definition for the FAP
def fitness_function(ind):
    penalization = 0
    for e in E:
        if abs(ind[e.i] - ind[e.j]) <= e.dij:
            penalization += e.pij
    
    return penalization,


"""
PART 2
SETUP DEAP framework parameters
"""
pop_size = 100  # population size
n_gen = 100  # number of generations
pm = 1.0 / n  # mutation probability
pcx = 1  # recombination probability
k = 2  # tournament selection

"""
weight:
    +1.0 for maximization
    -1.0 for minimization
"""
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)
toolbox = base.Toolbox()

# representation of individuals
toolbox.register("attr_int", random.randint, 0, F - 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n)

# representation of population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# set fitness function
toolbox.register("evaluate", fitness_function)

# set recombination operator
toolbox.register("mate", tools.cxTwoPoint)

# set mutation operator
toolbox.register("mutate", tools.mutUniformInt, low=0, up=F - 1, indpb=pm)

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
# get the execution time
elapsed_time = tm.time() - st
print('Execution time:', elapsed_time, 'seconds')

"""
PART 4
PLOT CONVERGENCE
"""
# get best individual ever seen
best_ind = hof.items.pop(0)

# plot convergence
fap_plotter.print_convergence([log[i]["Min"] for i in range(n_gen)], "fitness")
print(best_ind)
