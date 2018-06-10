#!/usr/bin/python2.7

'''
    File name: knapsack_problem.py 
    Author: Maria Petrisor
    Date created: 07/06/2018
    Python Version: 2.7
'''

import random
import math
import collections

class Knapsack:
    def __init__(self, config, max_capacity):
        self.config = config
        self.max_capacity = max_capacity

    def get_object_length(self, obj):
        return self.config[obj][0]

    def get_object_value(self, obj):
        return self.config[obj][1]

    def get_config(self):
        return self.config

    def get_config_length(self):
        return len(self.config)

    def get_max_capacity(self):
        return self.max_capacity

    def get_max_value(self):
        value = 0
        for entry in self.config:
            value += self.config[entry][1]
        return value


class GeneticAlgorithm:
    def __init__(self, knapsack_initial_config, population_size, iterations_number, crossover_rate, mutation_rate,
                 cloning_rate):
        self.knapsack = knapsack_initial_config
        self.population_size = population_size
        self.iterations_number = iterations_number
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.cloning_rate = cloning_rate
        self.iteration = 1

    def generate_initial_population(self, array_length):
        population = []
        for _ in range(0, self.population_size):
            population.append(''.join(random.choice(["0", "1"]) for _ in range(array_length)))
        return population

    def get_sol_total_value_capacity(self, solution):
        total_value = 0
        total_capacity = 0
        for index, entry in enumerate(solution):
            if entry == "1":
                total_value += self.knapsack.get_object_value(self.knapsack.get_config().keys()[index])
                total_capacity += self.knapsack.get_object_length(self.knapsack.get_config().keys()[index])

        return total_value, total_capacity

    # We want the capacity of the knapsack to be as near to the maximum (7) as possible --> 50%
    # and the total value of the objects to be as high as possible  --> 50%
    def fitness_function(self, solution):
        (total_value, total_capacity) = self.get_sol_total_value_capacity(solution)
        if total_capacity > self.knapsack.get_max_capacity():
            return 0
        else:
            return (total_capacity * 0.5)/float(self.knapsack.get_max_capacity()) + \
                   (total_value * 0.5)/float(self.knapsack.get_max_value())

    def get_choice_probability(self, s_current):
        return self.fitness_function(s_current)

    def select_solution(self, P_s_current):
        rand = random.uniform(0, 1)
        return rand <= P_s_current

    def crossover(self, s_1, s_2):
        crossover_point = int(random.uniform(0, self.knapsack.get_config_length() - 1))
        new_individual_1 = s_1[:crossover_point] + s_2[crossover_point:]
        new_individual_2 = s_2[:crossover_point] + s_1[crossover_point:]
        return new_individual_1, new_individual_2

    def mutation(self, s_current):
        gene_index = int(random.uniform(0, self.knapsack.get_config_length() - 1))
        s_list = list(s_current)
        if s_list[gene_index] == "0":
            s_list[gene_index] = "1"
        else:
            s_list[gene_index] = "0"
        return "".join(s_list)

    def clone_N_individuals(self, sorted_s, N):
        return sorted_s[:N]

    def genetic_algorithm(self, s):
        if self.iteration > self.iterations_number:
            return s

        print "\n~~~Iteration: {}~~~".format(self.iteration)

        s.sort(key=lambda k: self.fitness_function(k), reverse=True)

        new_s = []
        while len(new_s) < self.population_size*self.crossover_rate:
            s_current = []
            s_current.append(None)
            s_current.append(None)

            i = 0

            while i < 2:
                s_current[i] = s[int(random.uniform(0, self.population_size-1))]

                P_s_current = self.get_choice_probability(s_current[i])
                if self.select_solution(P_s_current):
                    i += 1

            s_1, s_2 = self.crossover(s_current[0], s_current[1])
            
            new_s.append(s_1)
            new_s.append(s_2)

        while len(new_s) < self.population_size*(self.crossover_rate + self.mutation_rate):
            s_current = s[int(random.uniform(0, self.population_size-1))]
            s_mutated = self.mutation(s_current)
            new_s.append(s_mutated)

        while len(new_s) < self.population_size*(self.crossover_rate + self.mutation_rate + self.cloning_rate):
            clones = self.clone_N_individuals(s, int(self.population_size*self.cloning_rate))  
            new_s.extend(clones)
        print new_s

        big_population = s + new_s
        big_population = list(set(big_population))
        big_population.sort(key=lambda k: self.fitness_function(k), reverse=True)

        if len(big_population) > population_size:
            new_s = big_population[:population_size]

        self.iteration += 1
        return self.genetic_algorithm(new_s)

if __name__ == "__main__":

    knapsack_config = collections.OrderedDict()
    knapsack_config["a"] = (3, 2)
    knapsack_config["b"] = (2, 4)
    knapsack_config["c"] = (1, 1)
    knapsack_config["d"] = (3, 6)
    knapsack_config["e"] = (2, 3)
    knapsack_config["f"] = (1, 3)

    knapsack = Knapsack(knapsack_config, 7)

    population_size = 10
    iterations_number = 100
    crossover_rate = 0.8
    mutation_rate = 0.15
    cloning_rate = 0.05

    algo = GeneticAlgorithm(knapsack, population_size, iterations_number, crossover_rate, mutation_rate, cloning_rate)

    s = algo.generate_initial_population(knapsack.get_config_length())

    s.sort(key=lambda k: algo.fitness_function(k), reverse=True)

    s_final = algo.genetic_algorithm(s)

    print "Best packing solutions: "
    for sol in s_final:
        print sol, algo.fitness_function(sol), algo.get_sol_total_value_capacity(sol)[0], \
            algo.get_sol_total_value_capacity(sol)[1]
