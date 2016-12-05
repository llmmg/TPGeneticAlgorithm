import sys
import pygame


class City:
    name = ""
    posx = 0
    posy = 0

    def __init__(self, name, posx, posy):
        self.name = name
        self.posx = posx
        self.posy = posy

    def __str__(self):
        return self.name + " " + self.posx + " " + self.posy


def draw_gui():
    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    def draw(positions):
        screen.fill(0)
        for pos in positions:
            pygame.draw.circle(screen, city_color, pos, city_radius)
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
                cities.append(pygame.mouse.get_pos())
                draw(cities)

    screen.fill(0)

    # ALGORITHM GOES HERE
    return cities

    # Draw best path we found
    pygame.draw.lines(screen, city_color, True, cities)
    text = font.render("Résultat", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            break


def load_from_file(file):
    with open(file, u'r') as f:
        cities = []
        lines = f.readlines()
        for line in lines:
            name, pos_x, pos_y = line.split()
            c = City(name, pos_x, pos_y)
            cities.append(c)

    return cities


def do(cities):
    print("DOOOOOO")


def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if file == None and gui == True:
        cities = draw_gui()
    elif file != None:
        cities = load_from_file(file)

    do(cities)


if __name__ == '__main__':
    ga_solve("ressources12/data/pb005.txt", False)
