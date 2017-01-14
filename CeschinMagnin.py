import math
import sys
import time
from random import randint, choice, shuffle

import pygame

# GLOBALS FOR GUI
screen_x = 500
screen_y = 500
window = None
screen = None
font = None


# ----------------------------
# City
# ----------------------------
class City:
    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y

    def __str__(self):
        return self._name

    def __eq__(self, city2):
        return self._x == city2.x() and self._y == city2.y()

    def __hash__(self):
        return hash(self._x, self._y, self._name)

    def calculate_distance(self, city2):
        return math.sqrt((city2.x() - self._x) ** 2 + (city2.y() - self._y) ** 2)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def name(self):
        return self._name


# ----------------------------
# Population
# ----------------------------
class Population:
    def __init__(self, list_solutions):
        self._listSolutions = list_solutions

    def __str__(self):
        string = ""
        for solution in self._listSolutions:
            string += str(solution) + "\n"
        return string

    def new_generation(self):
        pop_size = len(self._listSolutions)

        self.crossover(pop_size)
        self.mutate(pop_size)
        self.reduce_population(pop_size)

    def crossover(self, number_of_children):
        fitness_sum = 0
        for solution in self._listSolutions:
            fitness_sum += solution.distance()

        self._listSolutions = sorted(self._listSolutions, key=lambda sol: sol.distance())
        children_list = []
        for i in range(0, number_of_children):
            temp_sum = 0
            p0 = randint(0, int(fitness_sum))
            p1 = randint(0, int(fitness_sum))
            parent0 = None
            parent1 = None
            for solution in self._listSolutions:
                temp_sum += solution.distance()
                if temp_sum >= p0 and parent0 is None:
                    parent0 = solution
                if temp_sum >= p1 and parent1 is None:
                    parent1 = solution

                if parent0 is not None and parent1 is not None:
                    break

            child = parent0.cross(parent1)
            if child not in self._listSolutions and child not in children_list:
                children_list.append(child)
        self._listSolutions.extend(children_list)

    def mutate(self, pop_size):
        probability = 10
        # the more, the less solutions may be mutate
        elite_number = 5

        for solution in self._listSolutions[int(pop_size / 100 * elite_number):]:
            if randint(0, 100) <= probability:
                solution.mutate2()

    def reduce_population(self, pop_size):
        self._listSolutions = sorted(self._listSolutions, key=lambda sol: sol.distance())[:pop_size]
        '''
        new_list = self._listSolutions[:int(pop_size/2)]
        while len(new_list) < pop_size:
            solution = choice(self._listSolutions)
            if solution not in new_list:
                new_list.append(solution)
        self._listSolutions = sorted(new_list, key=lambda  sol: sol.distance())
        '''

    def get_best_solution(self):
        return self._listSolutions[0]


# ----------------------------
# Solution
# ----------------------------
class Solution:
    def __init__(self, cities):
        self._cities = cities
        self._distance = 0
        self.calculate_distance()

    def __str__(self):
        string = ""
        for city in self._cities:
            string += str(city)
            string += " - "

        string += str(self._distance)
        return string

    def __eq__(self, sol2):
        return self.cities() == sol2.cities()

    def __hash__(self):
        return hash(self._cities)

    def calculate_distance(self):
        self._distance = 0
        old_city = self.cities()[-1]
        for city in self.cities():
            self._distance += city.calculate_distance(old_city)
            old_city = city

    def mutate(self):
        index = randint(1, len(self.cities()) - 1)
        index2 = randint(1, len(self.cities()) - 1)
        self.cities()[index], self.cities()[index2] = self.cities()[index2], self.cities()[index]

        # tests
        # index = randint(1, len(self.cities()) - 1)
        # index2 = randint(1, len(self.cities()) - 1)
        # self.cities()[index], self.cities()[index2] = self.cities()[index2], self.cities()[index]
        self.calculate_distance()

    def mutate2(self):
        r=randint(1,2)
        for i in range(0,r):
            p1 = randint(1, len(self.cities()) - 1)
            p2 = randint(1, len(self.cities()) - 1)
            self.cities()[p1:p2] = reversed(self.cities()[p1:p2])

        self.calculate_distance()


    def cross(self, other_solution):

        cut_position = randint(1, len(self.cities()))

        self_part_1 = self.cities()[0:cut_position]
        for c in other_solution.cities():
            if c not in self_part_1:
                self_part_1.append(c)

        return Solution(self_part_1)

    def cross2(self, other_solution):
        """ Principe global de mutation : Mutation XO.
            Based on Axel Roy implementation
        """

        length = len(self.cities())
        start_xo_index = int(length / 2 - length / 4)
        end_xo_index = int(length / 2 + length / 4)

        # Détermination des valeurs à supprimer dans x, tirées de la portion y
        list_to_replace = other_solution.cities()[start_xo_index:end_xo_index + 1]

        empty_city = City("void", 0, 0)

        # Remplacement de ces valeurs dans x avec des None
        new_path = [value if value not in list_to_replace else empty_city for value in self.cities()]

        # Comptage du nombre de None à droite de la section (pour le décalage)
        nb_none_right = new_path[end_xo_index + 1:].count(empty_city)

        # Suppression des None dans la liste pour les rotations
        new_path = [value for value in new_path if value != empty_city]

        # Rotation à droite des éléments
        for counter in range(0, nb_none_right):
            new_path.insert(len(new_path), new_path.pop(0))
        list_to_insert = other_solution.cities()[start_xo_index:end_xo_index + 1]

        # Insertion des valeurs de y dans la section préparée
        new_path[start_xo_index:start_xo_index] = list_to_insert

        # Rotation pour avoir la meme valeur en 0 (afin d'éviter les doublons style A B C = B C A
        nb_rotation = new_path.index(self.cities()[0])
        new_path = new_path[nb_rotation:] + new_path[:nb_rotation]

        child = Solution(new_path)
        return child

    def cities(self):
        return self._cities

    def distance(self):
        return self._distance


def load_from_file(file):
    with open(file, u'r') as f:
        cities = []
        lines = f.readlines()
        for line in lines:
            name, pos_x, pos_y = line.split()
            c = City(name, int(pos_x), int(pos_y))
            cities.append(c)

    # add cities by cities with shortest distance
    shrt_cit = [cities.pop()]
    while len(cities) > 0:
        next_cit = find_closest_city(shrt_cit[-1], cities)
        cities.remove(next_cit)
        shrt_cit.append(next_cit)

    return shrt_cit


def find_closest_city(city, list_cit):
    tmp_dist = city.calculate_distance(list_cit[0])
    closest_city = list_cit[0]

    for cit in list_cit:
        current_dist = city.calculate_distance(cit)
        if current_dist < tmp_dist:
            closest_city = cit
            tmp_dist = current_dist

    return closest_city


def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    init_gui()
    # load cities from file and/or start collecting trough gui
    if file is not None:
        cities = load_from_file(file)
    if gui is True:
        # Loop for collecting cities
        collecting = True
        while collecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    collecting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cities.append(City("v" + str(len(cities)), pos[0], pos[1]))
                    draw(cities)

    # -----------------------
    # Main Loop
    # -----------------------

    population = generate_start_population(cities, 30)
    best_solution = population.get_best_solution()
    same_solution_counter = 0
    start_time = time.time()
    draw(population.get_best_solution())

    i = 0

    while same_solution_counter < 100 and (maxtime == 0 or (time.time() - start_time <= float(maxtime))):
        population.new_generation()
        # print(population)
        # print("------------------")
        i += 1
        if population.get_best_solution() == best_solution:
            same_solution_counter += 1
        else:
            same_solution_counter = 0
            best_solution = population.get_best_solution()
            draw(best_solution)

    print("DONE in " + str(i) + " iterations ")
    print(best_solution.distance())

    # ----------------------
    # Boucle pour rester dans l'affichage
    # ----------------------
    collecting = True
    while collecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                collecting = False
    screen.fill(0)
    pygame.quit()


# return a starting population
def generate_start_population(cities, population_size):
    """
    :param cities: list of whole cities
    :param population_size: size of the population
    :return: a population (many different solutions)
    """
    # solution list
    solList = []
    sol = []

    # cities is by default "sorted" (see file loading) so add it to solution before mixing
    # solList.append(Solution(cities))

    # generate solutions
    for i in range(0, population_size):
        sol = cities[1:]
        shuffle(sol)
        sol.insert(0, cities[0])
        new_solution = Solution(sol)
        if new_solution not in solList:
            solList.append(new_solution)

    return Population(solList)


# ----------------------
# GUI
# ----------------------

def init_gui():
    global window
    global screen
    global font

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Travelling Salesman')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)


def draw(item):
    # item can be a solution or a list of cities
    if type(item) is Solution:
        list_cities = item.cities()
    else:
        list_cities = item

    screen.fill(0)

    city_color = [0, 255, 0]
    city_radius = 5

    old_city = list_cities[-1]
    for city in list_cities:
        pygame.draw.circle(screen, city_color, (city.x(), city.y()), city_radius)

        # Create the label with the name of the city
        label = font.render(city.name(), 1, city_color, None)
        # Draw the label
        screen.blit(label, (city.x() + 10, city.y() - 6))
        # draw lines
        pygame.draw.line(screen, 0xffffff, (old_city.x(), old_city.y()), (city.x(), city.y()), 1)
        old_city = city

    pygame.display.flip()


if __name__ == '__main__':
    ga_solve("ressources12/data/pb100.txt", False, 60)
    # best for 50 = 2515
