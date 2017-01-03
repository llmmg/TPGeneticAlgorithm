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
        self._distancesSum = self.calculateDistance()

    def calculate_distance(self):
        pass

    def new_generation(self):
        pass

    def select_roulette(self):
        pass

    def select_elitism(self):
        pass

    def mutate(self):
        pass

    def cross(self):
        pass

    def elitism_experiment(self):
        pass

    def get_best_solutions(self):
        pass


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

    def __eq__(self, sol2):
        return self._problem.get_cities() == sol2.problem().get_cities()

    def calculate_distance(self):
        return 0

    def mutate(self):
        pass

    def cross(self):
        pass

    def problem(self):
        return self._problem


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
            print("appened")

    # Display generated solutions
    i = 0
    for sol in solList:
        i += 1
        print("solution ", i)
        for cit in sol.problem().get_cities():
            print(cit)

    # test
    # print("distance from", cities[0], " to ", cities[1])
    # print("dist=", cities[0].point().calculate_distance(cities[1].point()))

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
    pass


if __name__ == '__main__':
    # ga_solve()
    ga_solve("ressources12/data/pb005.txt", False)
