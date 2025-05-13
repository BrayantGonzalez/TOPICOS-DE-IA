import random
import numpy as np

# Definir las ciudades y sus distancias
cities = ["Vigo", "Celta", "Valladolid", "Madrid", "Sevilla", "Jaen", "Granada", "Murcia", "Valencia", "Barcelona", "Zaragoza", "Bilbao", "Gerona", "Albacete"]
distances = np.array([
    [0, 171, 235, 411, 245, 125, 244, 150, 349, 296, 324, 378, 289, 257],  # Vigo
    [171, 0, 193, 390, 211, 125, 207, 150, 241, 296, 215, 324, 289, 257],  # Celta
    [235, 193, 0, 193, 244, 125, 244, 150, 241, 296, 215, 324, 289, 257],  # Valladolid
    [411, 390, 193, 0, 245, 125, 244, 150, 241, 296, 215, 324, 289, 257],  # Madrid
    [245, 211, 244, 245, 0, 125, 244, 150, 241, 296, 215, 324, 289, 257],  # Sevilla
    [125, 125, 125, 125, 125, 0, 244, 150, 241, 296, 215, 324, 289, 257],  # Jaen
    [244, 207, 244, 244, 244, 244, 0, 150, 241, 296, 215, 324, 289, 257],  # Granada
    [150, 150, 150, 150, 150, 150, 150, 0, 241, 296, 215, 324, 289, 257],  # Murcia
    [349, 241, 241, 245, 245, 241, 241, 241, 0, 296, 215, 324, 289, 257],  # Valencia
    [296, 296, 296, 296, 296, 296, 296, 296, 296, 0, 215, 324, 289, 257],  # Barcelona
    [324, 215, 215, 215, 215, 215, 215, 215, 215, 215, 0, 324, 289, 257],  # Zaragoza
    [378, 324, 324, 324, 324, 324, 324, 324, 324, 324, 324, 0, 289, 257],  # Bilbao
    [289, 289, 289, 289, 289, 289, 289, 289, 289, 289, 289, 289, 0, 257],  # Gerona
    [257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 257, 0]   # Albacete
])

class GA_TSP:
    def __init__(self, distance_matrix, population_size=100, generations=500, mutation_rate=0.01, crossover_rate=0.9):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = self.initial_population()

    def initial_population(self):
        population = []
        for _ in range(self.population_size):
            individual = list(range(self.num_cities))
            random.shuffle(individual)
            population.append(individual)
        return population

    def fitness(self, individual):
        total_distance = 0
        for i in range(self.num_cities - 1):
            total_distance += self.distance_matrix[individual[i]][individual[i + 1]]
        total_distance += self.distance_matrix[individual[-1]][individual[0]]  # Return to the start city
        return 1 / total_distance  # Inverse of distance for fitness (higher is better)

    def selection(self):
        selected = random.choices(self.population, k=self.population_size)
        return selected

    def crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end + 1] = parent1[start:end + 1]
        pointer = 0
        for i in range(size):
            if child[i] == -1:
                while parent2[pointer] in child:
                    pointer += 1
                child[i] = parent2[pointer]
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.num_cities), 2)
            individual[i], individual[j] = individual[j], individual[i]

    def run(self):
        for generation in range(self.generations):
            selected = self.selection()
            new_population = []
            for i in range(0, self.population_size, 2):
                if random.random() < self.crossover_rate:
                    child1 = self.crossover(selected[i], selected[i + 1])
                    child2 = self.crossover(selected[i + 1], selected[i])
                else:
                    child1, child2 = selected[i], selected[i + 1]
                self.mutate(child1)
                self.mutate(child2)
                new_population.extend([child1, child2])
            self.population = new_population
            best_individual = max(self.population, key=lambda x: self.fitness(x))
            best_fitness = self.fitness(best_individual)
            print(f"Generation {generation}: Best Fitness = {best_fitness}")
        
        best_individual = max(self.population, key=lambda x: self.fitness(x))
        return best_individual, 1 / self.fitness(best_individual)

if __name__ == "__main__":
    ga = GA_TSP(distances, population_size=100, generations=500, mutation_rate=0.01, crossover_rate=0.9)
    best_route, best_distance = ga.run()
    print("Best route:", [cities[i] for i in best_route])
    print("Best distance:", best_distance)