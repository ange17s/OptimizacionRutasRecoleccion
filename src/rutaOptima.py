import numpy as np
import random
from alertas import obtenerAlertas

def calculate_total_distance(route, coordinates):
    # Función para calcular la distancia total de una ruta
    total_distance = 0
    coordinates = np.array(coordinates)
    for i in range(len(route)):
        start = coordinates[route[i]]
        end = coordinates[route[(i + 1) % len(route)]]
        total_distance += ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
    return total_distance

def initial_population(pop_size, num_points):
    population = []
    for _ in range(pop_size):
        individual = list(range(num_points))
        random.shuffle(individual)
        population.append(individual)
    return population

def rank_routes(population, coordinates):
    ranked_routes = []
    for i, route in enumerate(population):
        distance = calculate_total_distance(route, coordinates)
        ranked_routes.append((i, distance))
    ranked_routes.sort(key=lambda x: x[1])
    return ranked_routes

def selection(ranked_population, elite_size):
    selection_results = [ranked_population[i][0] for i in range(elite_size)]
    for _ in range(len(ranked_population) - elite_size):
        selected = random.choice(ranked_population)[0]
        selection_results.append(selected)
    return selection_results

def mutate(individual):
    """
    Mutación simple: intercambia dos genes aleatorios en un individuo.
    """
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def next_generation(current_gen, elite_size, mutation_rate, coordinates):
    population = []
    ranked_population = rank_routes(current_gen, coordinates)
    selection_results = selection(ranked_population, elite_size)
    
    selected_individuals = [current_gen[i] for i in selection_results]

    for i in range(elite_size):
        population.append(selected_individuals[i])
    
    for i in range(len(selected_individuals) - elite_size):
        parent1 = selected_individuals[i]
        parent2 = selected_individuals[len(selection_results) - i - 1]
        child = ordered_crossover(parent1, parent2)
        population.append(child)
    
    # Aplicar mutación aquí si es necesario
    return population


def ordered_crossover(parent1, parent2):
    child = [-1] * len(parent1)
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child[start:end] = parent1[start:end]

    remaining = [gene for gene in parent2 if gene not in child]
    current_pos = 0
    for i in range(len(child)):
        if child[i] == -1:
            child[i] = remaining[current_pos]
            current_pos += 1
    return child


def algoritmoGenetico(coordinates, pop_size, elite_size, mutation_rate, generations):
    num_points = len(coordinates)
    population = initial_population(pop_size, num_points)
    
    for generation in range(generations):
        print(f"Generation: {generation}")
        ranked_population = rank_routes(population, coordinates)
        population = next_generation(population, elite_size, mutation_rate, coordinates)
    
    ranked_population = rank_routes(population, coordinates)
    best_route_index = ranked_population[0][0]
    return population[best_route_index]

if __name__ == "__main__":
    # Obtener alertas y extraer coordenadas
    alertas = obtenerAlertas()
    #coordinates = np.array([alerta['coordinates'] for alerta in alertas])
    coordinates = [alerta['coordinates'] for alerta in alertas]
    # Parámetros del algoritmo genético
    pop_size = 3  # Tamaño de la población
    elite_size = 1  # Tamaño de la élite
    mutation_rate = 0.01  # Tasa de mutación
    generations = 10  # Número de generaciones

    # Ejecutar el algoritmo genético
    #best_route = algoritmoGenetico(coordinates, pop_size, elite_size, mutation_rate, generations)
    #best_route_coordinates = coordinates[best_route]

    best_route_coordinates = algoritmoGenetico(coordinates, pop_size, elite_size, mutation_rate, generations)

    # Imprimir la mejor ruta encontrada
    print("Mejor ruta encontrada:")
    #for idx in best_route:
    #    print(f"Alerta ID: {alertas[idx]['id']}, Coordenadas: {alertas[idx]['coordinates']}")
    for coords in best_route_coordinates:
        print(f"Coordenadas: {coords}")