import argparse
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
font_color = [100, 100, 100]


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
        return hash((self._x, self.y, self._name))

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
        """
        Transform this population into a new one (based on this one). This happens in 3 phases:
        1. add X children to the  population (parents are selected with a roulette selection)
        2. mutate the population (except the best solutions). This happens with a certain probability
        3. reduce size of the population to the same size we had before adding the children (remove the worst solutions)
        """
        pop_size = len(self._listSolutions)

        self.generate_children(int(pop_size))
        self.do_mutation(pop_size)
        self.reduce_population(pop_size)

    def generate_children(self, number_of_children):
        """
        Generate new solutions and add them to self._listSolutions.
        Parents are selected with a roulette algorithm
        :param number_of_children: number of children to create
        """
        children_list = []
        for i in range(0, number_of_children):
            parent0 = self.select_roulette()
            parent1 = self.select_roulette()

            child = parent0.cross(parent1)
            if child not in self._listSolutions and child not in children_list:
                children_list.append(child)
        self._listSolutions.extend(children_list)

    def do_mutation(self, pop_size):
        """
        Mutate the solutions with a probability to happens
        This doesnt affect the elite_number percentage of best solutions
        :param pop_size: size of the population ( without the children )
        """
        probability = 10
        elite_number = 10

        for solution in self._listSolutions[int(pop_size / 100 * elite_number):]:
            if randint(0, 100) <= probability:
                solution.mutate2()

        self._listSolutions = sorted(self._listSolutions, key=lambda sol: sol.distance())

    def reduce_population(self, pop_size):
        """
        Reduce the population (keep the bests)
        :param pop_size: size wanted for the population
        """
        self._listSolutions = sorted(self._listSolutions, key=lambda sol: sol.distance())[:int(pop_size)]

    def select_roulette(self):
        """
        Select a solution from self._listSolutions with roulette selection algorithm
        :return: a city
        """
        sorted_list = sorted(self._listSolutions, key=lambda sol: sol.distance())

        fitness_sum = 0
        for solution in self._listSolutions:
            fitness_sum += solution.distance()

        roulette = randint(0, int(fitness_sum))

        distance_sum = 0
        index = 0

        for solution in reversed(sorted_list):
            distance_sum += solution.distance()
            if distance_sum >= roulette:
                return sorted_list[index]
            index += 1

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
        """
        Calculate the distance of this solution
        """
        self._distance = 0
        old_city = self.cities()[-1]
        for city in self.cities():
            self._distance += city.calculate_distance(old_city)
            old_city = city

    def mutate(self):
        """
        Mutate a solution by swapping 2 cities
        """
        index = randint(1, len(self.cities()) - 1)
        index2 = randint(1, len(self.cities()) - 1)
        self.cities()[index], self.cities()[index2] = self.cities()[index2], self.cities()[index]

        self.calculate_distance()

    def mutate2(self):
        """
        Mutate a solution by reversing a block of cities. This happens 1 or 2 times (random)
        """
        r = randint(1, 2)
        for i in range(0, r):
            p1 = randint(1, len(self.cities()) - 1)
            p2 = randint(1, len(self.cities()) - 1)
            self.cities()[p1:p2] = reversed(self.cities()[p1:p2])

        self.calculate_distance()

    def cross(self, other_solution):
        """
        Cross in 1 point
        :param other_solution: other solution to cross with
        :return: a new solution (child of self and other_solution)
        """
        cut_position = randint(1, len(self.cities()))

        self_part_1 = self.cities()[0:cut_position]
        for c in other_solution.cities():
            if c not in self_part_1:
                self_part_1.append(c)

        return Solution(self_part_1)

    def cross2(self, other_solution):
        """
        Cross in 2 points
        Based on Axel Roy implementation
        :param other_solution: other solution to cross with
        :return: a new solution (child of self and other_solution)
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
    """
    :param file: file to load cities from
    :return: list of cities
    """
    with open(file, u'r') as f:
        cities = []
        lines = f.readlines()
        for line in lines:
            name, pos_x, pos_y = line.split()
            c = City(name, int(pos_x), int(pos_y))
            cities.append(c)

    return cities


def ga_solve(file=None, gui=True, maxtime=0):
    """
    :param file: file to load the cities from
    :param gui: add points trough clicking on the screen ?
    :param maxtime: maximum resolution time in seconds
    :return: a tuple of (distance, path) of the best solution
    """
    cities = []
    # load cities from file and/or start collecting trough gui
    if file is not None:
        cities = load_from_file(file)
    if gui:
        init_gui()
        draw(cities)

        text = font.render("press enter to start", True, font_color)
        textRect = text.get_rect(centerx=screen.get_width() / 2)
        screen.blit(text, textRect)
        pygame.display.flip()

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
    if gui:
        draw(population.get_best_solution())

    while same_solution_counter < 100 and (maxtime == 0 or (time.time() - start_time <= float(maxtime))):
        population.new_generation()
        if population.get_best_solution() == best_solution:
            same_solution_counter += 1
        else:
            same_solution_counter = 0
            best_solution = population.get_best_solution()
            if gui:
                draw(best_solution)

    return best_solution.distance(), [city.name() for city in best_solution.cities()]


# return a starting population
def generate_start_population(cities, population_size):
    """
    :param cities: list of whole cities
    :param population_size: size of the population
    :return: a population (many different solutions)
    """
    # solution list
    sol_list = []

    # cities is by default "sorted" (see file loading) so add it to solution before mixing
    # sol_list.append(Solution(cities))

    # generate solutions
    for i in range(0, population_size):
        sol = cities[1:]
        shuffle(sol)
        sol.insert(0, cities[0])
        new_solution = Solution(sol)
        if new_solution not in sol_list:
            sol_list.append(new_solution)

    return Population(sol_list)


# ----------------------
# GUI methods
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


# ----------------------
# Main
# ----------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TSP solver with genetic algorithm')

    parser.add_argument('filename', type=argparse.FileType('r'),
                        help="The file that contains the cities",
                        nargs="?")

    parser.add_argument('--nogui', action='store_const', dest='gui',
                        const='1',
                        help='Disable the GUI')

    parser.add_argument('--maxtime', action='store', dest='maxtime', type=int,
                        help='Set the maximum execution time')

    # get all parameters
    args = parser.parse_args()

    # default values
    p_max_time = 0
    p_GUI = True
    p_collecting = False

    if args.maxtime is not None:
        p_max_time = abs(args.maxtime)

    if args.gui is not None:
        p_GUI = False

    if args.filename is None:
        filename = None
    else:
        filename = args.filename.name

    result = ga_solve(filename, p_GUI, p_max_time)

    print("distance = " + str(result[0]))
    if p_GUI:
        text = font.render("complete", True, font_color)
        textRect = text.get_rect(centerx=screen.get_width() / 2, centery=screen.get_height() / 2)
        screen.blit(text, textRect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    sys.exit(0)
