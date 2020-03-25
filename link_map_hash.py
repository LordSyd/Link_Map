import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
width = 800
height = 802

screen = pygame.display.set_mode((width, height))
running = True


LEFT = 1
switch_draw_entrances = True
switch_draw_exits = True
switch_zoom = True
x = 0
y = 0


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Marker(pygame.sprite.Sprite):

    """
  used to draw the marker at a given position
    """

    def __init__(self, x, y, key, function):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)
        self.image.set_alpha(50)
        self.key = key

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = 20
        self.h = 20
        self.shift_x = 0
        self.shift_y = 0

        self.function = function

    def check_click(self, mouse):

        if self.rect.collidepoint(mouse):
            self.image.set_alpha(200)
            return True

        if not self.rect.collidepoint(mouse):
            self.image.set_alpha(50)

    def collide_check(self, mouse):
        return self.rect.collidepoint(mouse)

    def get_function(self):
        return self.function

    def get_marker_connection_pair_key(self):
        return self.key

    def render(self, display, shift_x, shift_y, zoom=False):
        self.shift_x = shift_x
        self.shift_y = shift_y

        items_list = list(BackGround.rect)
        width_bg = items_list[2]
        height_bg = items_list[3]
        zoom_factor = width / items_list[2]
        if zoom is False:
            display.blit(self.image, (self.rect.x +
                                      shift_x, self.rect.y + shift_y))
        else:
            display.blit(self.image, (self.rect.x *
                                      0.56, self.rect.y * 0.56))


class Connections:

    def __init__(self):
        self.switch = False
        self.con_dict = {}
        self.key_dict = []

    def generate_key(self, position):
        position_x, position_y = position
        instance_name = str(position_x) + str(position_y)
        return instance_name

    def add_entrance_or_exit(self, position):
        if not self.switch:
            key = self.generate_key(position)
            self.key_dict.append(key)
            self.con_dict[key] = position
            pos_x, pos_y = position
            new_key = key + "_entrance"
            new_key = Marker(pos_x - 10, pos_y - 10, key, "entrance")
            entrances.add(new_key)
            self.switch = True
        else:
            key = self.key_dict[-1]
            old_pos = self.con_dict[key]
            pos_x, pos_y = position
            new_key = key + "_exit"
            new_key = Marker(pos_x - 10, pos_y - 10, key, "exit")
            exits.add(new_key)
            self.con_dict[key] = [old_pos, position]
            self.switch = False

    def return_pos_pair(self, key):
        return self.con_dict[key]


def check_collision(pos):
    collide = False
    for s in entrances:
        if s.check_click(pos) == True:
            collide = True
            return collide, s.get_marker_connection_pair_key()
    for s in exits:
        if s.check_click(pos) == True:
            collide = True
            return collide, s.get_marker_connection_pair_key()
    return collide, None


def limit(num, minimum=0, maximum=255):
    return max(min(num, maximum), minimum)


def calculate_shift(x, y):
    items_list = list(BackGround.rect)
    width_bg = items_list[2]
    height_bg = items_list[3]
    zoom_factor = items_list[2] / width
    new_x = (width / 2) - (x * zoom_factor)
    new_y = (height / 2) - (y * zoom_factor)
    real_x = limit(new_x, (width - width_bg), 0)
    real_y = limit(new_y, (height - height_bg), 0)
    return int(real_x), int(real_y)


mouse_x = 0
mouse_y = 0
new_x = 0
new_y = 0

entrances = pygame.sprite.Group()
exits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

connections = Connections()

while running:
    BackGround = Background('darkworld_large_recalc.jpg', [0, 0])

    key = pygame.key.get_pressed()

    if switch_zoom is False:
        new_x, new_y = calculate_shift(mouse_x, mouse_y)
        screen.blit(BackGround.image, (new_x, new_y))
    if switch_zoom is True:
        screen.blit(pygame.transform.scale(
            BackGround.image, (width, height)), BackGround.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            if collide is False or collide == None:
                mouse = pygame.mouse.get_pos()
                new_mouse_x, new_mouse_y = mouse
                x_background = new_mouse_x + abs(new_x)
                y_background = new_mouse_y + abs(new_y)
                position_background = (x_background, y_background)

                connections.add_entrance_or_exit(position_background)
            elif collide is True:
                print(connections.return_pos_pair(colliding_marker_key))
        if key[pygame.K_w]:
            if switch_zoom is True:

                mouse_x, mouse_y = pygame.mouse.get_pos()
                switch_zoom = False
                print(calculate_shift(mouse_x, mouse_y))
            else:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                switch_zoom = True

        if key[pygame.K_a]:
            if switch_draw_entrances is True:
                switch_draw_entrances = False
            else:
                switch_draw_entrances = True
        if key[pygame.K_d]:
            if switch_draw_exits is True:
                switch_draw_exits = False
            else:
                switch_draw_exits = True

    mouse = pygame.mouse.get_pos()
    mouse_xx, mouse_yy = mouse

    real_xx = mouse_xx + abs(new_x)
    real_yy = mouse_yy + abs(new_y)

    collide, colliding_marker_key = check_collision((real_xx, real_yy))

    entrances.update()
    exits.update()
    if switch_draw_entrances is True and switch_zoom is False:
        for entrance in entrances:

            entrance.render(screen, new_x, new_y)
            print(entrance.rect.x, entrance.rect.y, entrance.rect)
    if switch_draw_exits is True and switch_zoom is False:
        for exit in exits:

            exit.render(screen, new_x, new_y)
    if switch_draw_exits is True and switch_zoom is True:
        for exit in exits:

            exit.render(screen, new_x, new_y, True)
    if switch_draw_entrances is True and switch_zoom is True:

        for entrance in entrances:

            entrance.render(screen, new_x, new_y, True)
    pygame.display.update()
    clock.tick(40)


pygame.quit()
