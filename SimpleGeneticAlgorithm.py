"""
CIS 579 - Artificial Intelligence
Assignemnt 2
Author: Nicholas Butzke

Program prints out the fitness of the best individual in the current population and
the average fitness of the population as a whole.
A run terminates if a string of ten ones is found:
“1111111111”
"""
import random
import numpy as np
import time

"""
Function to return a random genome (bit string) of a given length
Arg1: length of the bit string                                      |           int

Return: bit string                                                  |           str
"""
def randomGenome(length: int) -> str:
    genome = ""
    for i in range(length):
        genome += str(random.choice([0,1]))
    return genome

"""
Function to return a new randomly created population of the specified size, represented as a list of genomes of the specified length.
Arg1: size of the population                                                      |           int
Arg2: length of each genome in the population                                     |           int

Return: list of genomes                                                           |           list[str]
"""
def makePopulation(size: int, length: int) -> list:
    population: list = []
    for i in range(size):
        population.append(randomGenome(length))
    return population

"""
Function to return the fitness value of a genome.
Arg1: bit string                                                                      |           str

Return: quantity of 1s in the genome                                                  |           int
"""
def fitness(genome: str) -> int:
    return genome.count('1')

"""
Returns a pair of values: the average fitness of the
population as a whole and the fitness of the best individual in the population with its index
Arg1: list of genomes                                                                      |           list[str]

Return: average fitness of the population, tuple[index of found, max fitness]              |           float, tuple[int, float]
"""
def evaluateFitness(population: list) -> float:
    fitList: list = np.empty([0,2])
    for i, ele in enumerate(population):
        # calculate the fitness of every genome and the store it as a tuple of the index and the fitness
        fitList = np.append(fitList, [[i, fitness(ele)]], axis = 0)
    # I want to return a tuple as the second return because the index of the most fit genome will prevent needing to search for it in the future
    return float(np.average(fitList[:, 1], axis=0)), max(fitList, key=lambda x: x[1])

"""
Selects and returns two genomes from the given population using
fitness-proportionate selection.
Arg1: list of genomes                                                                 |           list[str]

Return: Two genomes with the highest fitness                                          |           str, str
"""
def selectPair(population: list) -> str:
    avgFit, NULL = evaluateFitness(population)
    weights = [] # this will allow the random.choices() method to give a fitness-proportionate output
    for ele in population:
        weights.append(int(((fitness(ele)/avgFit)/len(population))*100))
    
    g1 = random.choices(population, weights)[0]
    g2 = random.choices(population, weights)[0]
    
    return g1, g2

"""
Returns two new genomes produced by crossing over the
given genomes at a random crossover point.
Arg1: bit string                                                                 |           str
Arg2: bit string                                                                 |           str

Return: bit string of the two input genomes spliced together                     |           str
"""
def crossover(genome1: str, genome2: str) -> str:
    crossoverPoint = random.randrange(0, len(genome1)-1)
    return genome1[:crossoverPoint] + genome2[crossoverPoint:]

"""
Returns a new mutated version of the given genome.
Arg1: bit string                                                                 |           str
Arg2: probability that a bit will mutate (flip)                                  |           float

Return: bit string of the input genome post mutation                             |           str
"""
def mutate(genome: str, mutationRate: float) -> str:
    newGenome = ""
    for c in genome:
        # each character will have a chance, based off the mutationRate, to bit flip or mutate
        if random.randrange(0,99,1) <= mutationRate*100:
            newGenome += str(int(c) ^ 1)
        else:
            newGenome += c
    return newGenome

"""
The main GA procedure, which
takes the population size, crossover rate (pc), and mutation rate (pm) as parameters. The
GA terminates at 30 runs or when which the string of all ones was found. This function
should return the generation number when it terminates.

Arg1: size of each generation                                                    |           int
Arg2: how frequently a crossover will occur                                      |           float
Arg3: how frequently a mutation will occur                                       |           float

Return: generation number                                                        |           int
"""
def runGA(populationSize: int, crossoverRate: float, mutationRate: float):
    # initial generation
    genome: str = ""
    count: int = 0
    population = makePopulation(populationSize, 10)
    avgFit, m = evaluateFitness(population)
    genome = population[int(m[0])]
    print("Generation   " + str(count) + ": average fitness " + "{:.2f}".format(avgFit) + ", best fitness " + "{:.2f}".format(m[1]))

    while(genome != "1"*10 and count < 30): # end condition of the run.  Will compare with the highest fitness genome
        count += 1
        if random.randrange(0,99,1) <= int(crossoverRate*100):
            # crossover 2 genomes
            pair = selectPair(population)
            genome = crossover(pair[0], pair[1])
        genome = mutate(genome, mutationRate)
        population = makePopulation(len(population)-1, 10) # generates a new population with space for the highest fitness genome
        population.append(genome) # carries over the highest fitness genome to the novel population
        avgFit, m = evaluateFitness(population)
        genome = population[int(m[0])] # grabs the highest fitness genome
        print("Generation   " + str(count) + ": average fitness " + "{:.2f}".format(avgFit) + ", best fitness " + "{:.2f}".format(m[1]))
    return count

def main():
    populationSize = 50
    print("Population size: " + str(populationSize))
    print("Genome length: " + str(10))
    runLimit = 10000
    genList = []
    startTime = time.time()
    for r in range(runLimit):
        print("Run: " + str(r))
        genList.append(runGA(populationSize, 0, 0.001))
    runTime = time.time() - startTime
    print("Average Generations: " + "{:.2f}".format(np.average(genList)))
    print("Runtime: " + format(runTime, ".5f") + "s")

if __name__ == "__main__":
    main()