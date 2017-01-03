import copy
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
        elite_percent = 20
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
            child.mutate()
            if child not in new_list_solution:
                return child

    def select_elitism(self, number):
        sorted_list = sorted(self._listSolutions, key=lambda sol: sol.distance())
        return copy.deepcopy(sorted_list[0:number])

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

    def set_cities(self,newCities):
        self._cities=newCities


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
        index = randint(2, len(cit) - 1)
        cit[index], cit[1] = cit[1], cit[index]

    def cross2(self, otherSol):
        cit = self._problem.get_cities()
        pt = randint(2, self._problem.get_size() - 2)
        print("index",pt)
        # cross with second part
        seq1 = []
        seq2 = []
        othCit = otherSol.problem().get_cities()

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

        # cit=new1
        self._problem.set_cities(new1)
        # othCit=new2
        otherSol.problem().set_cities(new2)

                # # entre 0,1 et rand-1,rand
                # # [1,rand[
                # seq1 = []
                # seq2 = []
                # # cities between cross points (0,rand)
                # for i in range(1, pt):
                #     seq1.append(cit[i])
                #     seq2.append(otherSol.problem().get_cities()[i])


    def cross(self, otherSolution):
        cut_position = randint(2, self._problem.get_size() - 2)

        self_part_1 = self._problem.get_cities()[0:cut_position]
        for c in otherSolution.problem().get_cities():
            if c not in self_part_1:
                self_part_1.append(c)

        return Solution(Problem(self_part_1))

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

    #cross test
    print("----CROSS TESTS---")
    print("sol 10=")
    for cit in solList[9].problem().get_cities():
        print(cit)

    print("sol 11=")
    for cit in solList[10].problem().get_cities():
        print(cit)

    print("---10 CROSS 11---")

    solList[9].cross2(solList[10])

    print("sol 10=")
    for cit in solList[9].problem().get_cities():
        print(cit)

    print("sol 11=")
    for cit in solList[10].problem().get_cities():
        print(cit)


    # for i in range(1, 200):
    #    population.new_generation()
    #    print(i, " new gen way=", population.get_best_solution().distance())

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
    ga_solve("ressources12/data/pb100.txt", False)
