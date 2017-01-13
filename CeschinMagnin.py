import math
import sys
import time
from random import randint

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
    def __init__(self, name, point):
        self._name = name
        self._point = point

    def __str__(self):
        return self._name

    def __eq__(self, city2):
        return self.point() == city2.point()

    def __hash__(self):
        return hash(self._point, self._name)

    def point(self):
        return self._point

    def name(self):
        return self._name


# ----------------------------
# Point
# ----------------------------
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return str(self._x) + " ; " + str(self._y)

    def __hash__(self):
        return hash(self._x, self._y)

    def calculate_distance(self, point):
        return math.sqrt((point.x() - self._x) ** 2 + (point.y() - self._y) ** 2)
        # return 1

    def x(self):
        return self._x

    def y(self):
        return self._y

    def coords(self):
        return self._x, self._y


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
        self.crossover(int(pop_size /2))
        self.mutate()
        self.reduce_population(pop_size)



    def crossover(self, number_of_children):
        fitness_sum = 0
        for solution in self._listSolutions:
            fitness_sum += solution.distance()

        self._listSolutions = sorted(self._listSolutions, key=lambda sol: sol.distance())
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
            if child not in self._listSolutions:
                self._listSolutions.append(child)

        self._listSolutions = sorted(self._listSolutions, key=lambda sol: sol.distance())

    def mutate(self):
        probability = 20
        eliteNumber = 20
        for solution in self._listSolutions[eliteNumber:]:
            if randint(0, 100) <= probability:
                solution.mutate()

    def reduce_population(self, pop_size):
        self._listSolutions = self._listSolutions[:pop_size]

    def select_elitism(self, number):
        sorted_list = sorted(self._listSolutions, key=lambda sol: sol.distance())
        return (sorted_list[0:number])[:]

    def get_best_solution(self):
        return self._listSolutions[0]


# ----------------------------
# Path
# ----------------------------
class Path:
    def __init__(self, cities):
        self._cities = cities

    def __eq__(self, prob):
        return self._cities == prob.cities()

    def __str__(self):
        string = ""
        for city in self._cities:
            string += str(city)
            string += " - "
        return string

    def __hash__(self):
        return hash(self._cities)

    def add_city(self, city):
        self._cities.append(city)

    def get_size(self):
        return len(self._cities)

    def cities(self):
        return self._cities[:]

    def set_cities(self, newCities):
        self._cities = newCities


# ----------------------------
# Solution
# ----------------------------
class Solution:
    def __init__(self, path):
        self._path = path
        # self._distance = 0
        self.calculate_distance()

    def __str__(self):
        return str(self._path) + str(self._distance)

    def __eq__(self, sol2):
        return self.path() == sol2.path()

    def __hash__(self):
        return hash(self._path)

    # @profile
    def calculate_distance(self):
        self._distance = 0
        old_point = self._path.cities()[-1].point()
        for city in self._path.cities():
            self._distance += city.point().calculate_distance(old_point)
            old_point = city.point()

    def mutate(self):
        index = randint(2, self.path().get_size() - 1)
        index2 = randint(1,  self.path().get_size() - 2)
        self.path()._cities[index], self.path()._cities[index2] = self.path()._cities[index2], self.path()._cities[index]

    def cross(self, otherSolution):

        cut_position = randint(1, self.path().get_size())

        self_part_1 = self.path().cities()[0:cut_position]
        for c in otherSolution.path().cities():
            if c not in self_part_1:
                self_part_1.append(c)

        return Solution(Path(self_part_1))

    def cross2(self, otherSolution):
        """ Principe global de mutation : Mutation XO.
            Based on Axel Roy implementation
        """
        try:
            start_xo_index = int(len(self._path.cities()) / 2 - len(self._path.cities()) / 4)
            end_xo_index = int(len(self._path.cities()) / 2 + len(self._path.cities()) / 4)

            # Détermination des valeurs à supprimer dans x, tirées de la portion y
            list_to_replace = otherSolution.path().cities()[start_xo_index:end_xo_index + 1]

            empty_city = City("void", Point(0, 0))

            # Remplacement de ces valeurs dans x avec des None
            new_path = [value if value not in list_to_replace else empty_city for value in self._path.cities()]

            # Comptage du nombre de None à droite de la section (pour le décalage)
            nb_none_right = new_path[end_xo_index + 1:].count(empty_city)

            # Suppression des None dans la liste pour les rotations
            new_path = [value for value in new_path if value != empty_city]

            # Rotation à droite des éléments
            for counter in range(0, nb_none_right):
                new_path.insert(len(new_path), new_path.pop(0))
            list_to_insert = otherSolution.path().cities()[start_xo_index:end_xo_index + 1]

            # Insertion des valeurs de y dans la section préparée
            new_path[start_xo_index:start_xo_index] = list_to_insert
            p = Path(new_path)
            child = Solution(p)
            return child

        except AttributeError:
            print("There's no item with that code")

    def path(self):
        return self._path

    def distance(self):
        return self._distance


def load_from_file(file):
    with open(file, u'r') as f:
        cities = []
        lines = f.readlines()
        for line in lines:
            name, pos_x, pos_y = line.split()
            c = City(name, Point(int(pos_x), int(pos_y)))
            cities.append(c)

    # add cities by cities with shortest distance
    shrtCit = []
    shrtCit.append(cities.pop())
    while(len(cities)>0):
        nextCit=closestCit(shrtCit[-1], cities)
        cities.remove(nextCit)
        shrtCit.append(nextCit)

    return shrtCit


def closestCit(city, listCit):
    tmpdist = city.point().calculate_distance(listCit[0].point())
    closestCity = listCit[0]

    for cit in listCit:
        curDist = city.point().calculate_distance(cit.point())
        if curDist < tmpdist:
            closestCity = cit
            tmpdist = curDist

    return closestCity


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
                    cities.append(City("v" + str(len(cities)), Point(pos[0], pos[1])))
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
        print(population)
        print("------------------")
        i += 1
        if population.get_best_solution() == best_solution:
            same_solution_counter += 1
        else:
            same_solution_counter = 0
            best_solution = population.get_best_solution()
            draw(best_solution)

    draw(best_solution)
    print("DONE in " + str(i) + " iterations ")
    # for cit in best_solution.path().cities():
    #     print(cit)

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
def generate_start_population(cities, populationSize):
    """
    :param cities: list of whole cities
    :param populationSize: size of the population
    :return: a population (many different solutions)
    """
    # solution list
    solList = []
    sol = []
    # mix iterations
    nbPass = len(cities)

    # cities is by default "sorted" (see file loading) so add it to solution before mixing
    # solList.append(Solution(Path(cities)))

    # generate solutions
    for i in range(0, populationSize):
        sol = cities[:]
        for j in range(0, nbPass):
            index = randint(1, len(cities) - 1)
            sol[index], sol[1] = sol[1], sol[index]
        new_solution = Solution(Path(sol))
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
        list_cities = item.path().cities()
    else:
        list_cities = item

    screen.fill(0)
    pointlist = []

    city_color = [0, 255, 0]
    city_radius = 5

    for city in list_cities:
        pos = city.point()
        # Points array for drawing lines between cities
        pointlist.append((pos.x(), pos.y()))
        pygame.draw.circle(screen, city_color, (pos.x(), pos.y()), city_radius)

        # Create the label with the name of the city
        label = font.render(city.name(), 1, city_color, None)
        # Draw the label
        screen.blit(label, (pos.x() + 10, pos.y() - 6))

    # draw lines

    oldpoint = pointlist[-1]
    for point in pointlist:
        # Draw the line between cities
        pygame.draw.line(screen, 0xffffff, oldpoint, point, 2)
        oldpoint = point

    pygame.display.flip()


if __name__ == '__main__':
    ga_solve("ressources12/data/pb050.txt", False)
    # best for 50 = 2515
