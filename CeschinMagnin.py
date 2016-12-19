import sys
import pygame
from random import randint


class City:
    name = ""
    posx = 0
    posy = 0

    def get_pos(self):
        return self.posx, self.posy

    def __init__(self, name, posx, posy):
        self.name = name
        self.posx = posx
        self.posy = posy

    def __str__(self):
        return self.name + " " + str(self.posx) + " " + str(self.posy)


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
            c = City(name, int(pos_x), int(pos_y))
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
            pygame.draw.circle(screen, city_color, city.get_pos(), city_radius)
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
    nbSolutions = 100
    nbPass = 10

    # generate 100 cities
    for i in range(0, nbSolutions):
        newSol=generateRnd(cities, nbPass)
        if newSol not in solList:
            solList.append(newSol)

    # Display generated solutions
    i = 0
    for sol in solList:
        i += 1
        print("solution ", i)
        for cit in sol:
            print(cit)

    # Natural selection => keep only x best solutions


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
