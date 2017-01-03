import sys
import pygame
import math
from random import randint


# ----------------------------
# City
# ----------------------------
class City:
    def __init__(self, name, point):
        self._name = name
        self._point = point

    def __str__(self):
        return self._name + " at position " + str(self._point)

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
        # create a new gen, and put it in _listolutions
        # 1 choisir les elites
        # 2 choisir des sol deja dans la pop
        # 3 faire des enfants pour completer
        pass

    def select_roulette(self):
        # select random sol from this population
        pass

    def select_elitism(self):
        # select top x%
        pass

    def mutate(self):
        """ Mutate some chromosome. We know list is sorted,
            we are going to keep the 10% bests and mutate the others """
        pass

    def cross(self):
        """ CrossOver some chromosome the population with a fifty percent chance to happen.
            The 5% of elits won't be affected. """
        pass

    def get_best_solution(self):
        return sorted(self._listSolutions, key=lambda sol: sol.distance())[0]


# ----------------------------
# Problem
# ----------------------------
class Problem:
    def __init__(self, cities):
        self._cities = cities

    def __eq__(self, prob):
        return self._cities == prob.get_cities()

    def add_city(self, city):
        self._cities.append(city)

    def get_size(self):
        return len(self._cities)

    def get_cities(self):
        return self._cities


# ----------------------------
# Solution
# ----------------------------
class Solution:
    def __init__(self, problem):
        self._problem = problem
        self._distance = 0
        self.calculate_distance()

    def __eq__(self, sol2):
        return self._problem.get_cities() == sol2.problem().get_cities()

    def calculate_distance(self):
        self._distance = 0
        cities = self._problem.get_cities()
        for i in range(0, self._problem.get_size() - 1):
            self._distance += cities[i].point().calculate_distance(cities[i + 1].point())
        # add distance from last city to start city (to complete the loop)
        self._distance += cities[0].point().calculate_distance(cities[-1].point())

    def mutate(self):
        cit = self._problem.get_cities()
        # cit = curentProb.cities
        index = randint(1, len(cit) - 1)
        cit[index], cit[1] = cit[1], cit[index]

    def cross(self):
        pass

    def problem(self):
        return self._problem

    def distance(self):
        return self._distance


def draw_gui():
    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Input')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    def draw(positions):
        screen.fill(0)
        for city in positions:
            pygame.draw.circle(screen, city_color, city.get_pos(), city_radius)
        text = font.render("Nombre: %i" % len(positions), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    cities = []
    draw(cities)

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

    screen.fill(0)
    pygame.quit()

    return cities


def load_from_file(file):
    with open(file, u'r') as f:
        cities = []
        lines = f.readlines()
        for line in lines:
            name, pos_x, pos_y = line.split()
            c = City(name, Point(int(pos_x), int(pos_y)))
            cities.append(c)

    return cities


def do(cities):
    # -----------------------
    # Affichage des villes
    # -----------------------
    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Results')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    def draw(positions):
        screen.fill(0)
        for city in cities:
            pygame.draw.circle(screen, city_color, city.point().coords(), city_radius)
        text = font.render("Nombre: %i" % len(positions), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    draw(cities)

    # ---------------------
    # Algorithm
    # ---------------------

    # Generate random lists (rnd orders)
    # solution list
    solList = []
    solList2 = []
    nbSolutions = 100

    # mix iterations
    nbPass = 10

    # generate 100 cities
    for i in range(0, nbSolutions):
        prob = Problem(generateRnd(cities, nbPass))
        newSolution = Solution(prob)
        if newSolution not in solList:
            solList.append(newSolution)

    # Display generated solutions
    i = 0
    for sol in solList:
        i += 1
        print("solution ", i)
        for cit in sol.problem().get_cities():
            print(cit)

    population = Population(solList)

    print("shortest way=", population.get_best_solution().distance())

    # Natural selection => keep only x best solutions
    # keep 3/4 best



    # Cross => childs


    # Mutations GOTO: natural selection
    ## GOTO: while loop with condition like 20 time loop or 20% is good...

    # ----------------------
    # Affichage du chemin
    # ----------------------


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


# return a list of rndm cities (= one solution)
def generateRnd(cities, nPass):
    """
    :param cities: list of whole cities
    :param nPass: number of mix pass. more passes = more random solutions
    :return: a solution (list of cities in random order)
    """
    sol = cities[:]

    # todo: 9% of chance to add the closest city next

    # mix the sol list
    for i in range(0, nPass):
        index = randint(1, len(sol) - 1)
        sol[index], sol[1] = sol[1], sol[index]

    return sol[:]


def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if file == None and gui == True:
        cities = draw_gui()
    elif file != None:
        cities = load_from_file(file)

    do(cities)


if __name__ == '__main__':
    # ga_solve()
    ga_solve("ressources12/data/pb005.txt", False)
