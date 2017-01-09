import copy
import sys
import pygame
import math
from random import randint

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
        return self._name + " at position " + str(self._point)

    def __eq__(self, city2):
        return self._name == city2.name()

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

    def calculate_distance(self, point):
        return math.sqrt((point.x() - self.x()) ** 2 + (point.y() - self.y()) ** 2)

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
    def __init__(self, listSolutions):
        self._listSolutions = listSolutions

    def new_generation(self):
        new_list_solution = list()
        population_size = len(self._listSolutions)

        # select elites
        elite_percent = 30
        elite_size = int(population_size * elite_percent / 100)
        new_list_solution.extend(self.select_elitism(elite_size))

        # select cross
        new_list_solution.extend([self.select_cross(new_list_solution) for i in range(population_size - elite_size)])

        self._listSolutions = new_list_solution

    def select_cross(self, new_list_solution):
        # select random sol from this population
        while True:
            i1 = randint(0, len(self._listSolutions) - 1)
            i2 = randint(0, len(self._listSolutions) - 1)
            child = self._listSolutions[i1].cross(self._listSolutions[i2])

            # test - mutate randomly
            iMut = randint(0, 3)
            if iMut == 0:
                child.mutate()

            if child not in new_list_solution:
                return child

    def select_elitism(self, number):
        sorted_list = sorted(self._listSolutions, key=lambda sol: sol.distance())
        return (sorted_list[0:number])[:]

    def get_best_solution(self):
        return sorted(self._listSolutions, key=lambda sol: sol.distance())[0]


# ----------------------------
# Path
# ----------------------------
class Path:
    def __init__(self, cities):
        self._cities = cities

    def __eq__(self, prob):
        return self._cities == prob.get_cities()

    def add_city(self, city):
        self._cities.append(city)

    def get_size(self):
        return len(self._cities)

    def get_cities(self):
        return self._cities[:]

    def set_cities(self, newCities):
        self._cities = newCities


# ----------------------------
# Solution
# ----------------------------
class Solution:
    def __init__(self, path):
        self._path = path
        self._distance = 0
        self.calculate_distance()

    def __eq__(self, sol2):
        return self.path().get_cities() == sol2.path().get_cities()

    def calculate_distance(self):
        self._distance = 0
        cities = self.path().get_cities()
        for i in range(0, self.path().get_size() - 1):
            self._distance += cities[i].point().calculate_distance(cities[i + 1].point())
        # add distance from last city to start city (to complete the loop)
        self._distance += cities[0].point().calculate_distance(cities[-1].point())

    def mutate(self):
        cit = self.path().get_cities()
        index = randint(2, len(cit) - 1)
        cit[index], cit[1] = cit[1], cit[index]

    def cross2(self, otherSol):
        cit = self.path().get_cities()
        pt = randint(2, self.path().get_size() - 2)

        # cross with second part
        seq1 = []
        seq2 = []
        othCit = otherSol.path().get_cities()

        for i in range(pt, len(cit)):
            seq1.append(cit[i])
            seq2.append(othCit[i])

        new1 = []
        new2 = []
        for i in range(0, len(cit)):
            if cit[i] not in seq2:
                new1.append(cit[i])
            if othCit[i] not in seq1:
                new2.append(othCit[i])

        new1.extend(seq2)
        new2.extend(seq1)

        self.path().set_cities(new1)
        otherSol.path().set_cities(new2)

        return otherSol

    def cross(self, otherSolution):
        cut_position = randint(2, self.path().get_size() - 2)

        self_part_1 = self.path().get_cities()[0:cut_position]
        for c in otherSolution.path().get_cities():
            if c not in self_part_1:
                self_part_1.append(c)

        return Solution(Path(self_part_1))

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

    return cities


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
    # Résultats
    # -----------------------
    population = generateStartPopulation(cities, 100)

    for i in range(1, 200):
        draw(population.get_best_solution())
        print(i, " path distance = ", population.get_best_solution().distance())
        population.new_generation()

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
def generateStartPopulation(cities, populationSize):
    """
    :param cities: list of whole cities
    :param populationSize: size of the population
    :return: a population (many different solutions)
    """
    # solution list
    solList = []
    sol = []
    # mix iterations
    nbPass = 10

    # generate solutions
    for i in range(0, populationSize):
        sol = cities[:]
        for j in range(0, nbPass):
            index = randint(1, len(cities) - 1)
            sol[index], sol[1] = sol[1], sol[index]
        newSolution = Solution(Path(sol))
        if newSolution not in solList:
            solList.append(newSolution)

    print(len(solList))
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
        list_cities = item.path().get_cities()
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

    # Don't forget to set the first element as the last too (close the loop)
    if len(pointlist) > 0:
        pointlist.append((pointlist[0]))
        # Draw the lines between cities
        pygame.draw.lines(screen, 0xffffff, False, [p for p in pointlist], 2)

    pygame.display.flip()


if __name__ == '__main__':
    ga_solve("ressources12/data/pb050.txt", False)
    # best for 50 = 2515
