import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
clock.tick(20)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((500, 500))
running = True


LEFT = 1
switch_draw_entrances = True
switch_draw_exits = True


class Marker(pygame.sprite.Sprite):

  """
used to draw the marker at a given position
  """

  def __init__(self, x, y, key, function):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface((50, 50))
    self.image.fill(RED)
    self.image.set_alpha(50)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

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
      new_key = Marker(pos_x, pos_y, key, "entrance")
      entrances.add(new_key)
      self.switch = True
    else:
      key = self.key_dict[-1]
      old_pos = self.con_dict[key]
      pos_x, pos_y = position
      new_key = key + "_exit"
      new_key = Marker(pos_x, pos_y, key, "exit")
      exits.add(new_key)
      self.con_dict[key] = [old_pos, position]
      self.switch = False

  def return_pos_pair(self, key):
    return self.con_dict[key]


entrances = pygame.sprite.Group()
exits = pygame.sprite.Group()

connections = Connections()


def check_collision(pos):
  collide = False
  for s in entrances:
    if s.check_click(pos) == True:
      collide = True
      return collide
  for s in exits:
    if s.check_click(pos) == True:
      collide = True
      return collide
  return collide


def switch_draw_markers(id):
  if id == "entrances":
    if switch_draw_entrances is True:
      switch_draw_entrances = False
    else:
      switch_draw_entrances = True
  if id == "exits":
    if switch_draw_exits is True:
      switch_draw_exits = False
    else:
      switch_draw_exits = True


while running:

  key = pygame.key.get_pressed()

  mouse = pygame.mouse.get_pos()
  collide = check_collision(mouse)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
      if collide == False or collide == None:
        mouse = pygame.mouse.get_pos()
        connections.add_entrance_or_exit(mouse)
    elif key[pygame.K_a]:
      if switch_draw_entrances is True:
        switch_draw_entrances = False
      else:
        switch_draw_entrances = True
    elif key[pygame.K_d]:
      if switch_draw_exits is True:
        switch_draw_exits = False
      else:
        switch_draw_exits = True

  screen.fill(BLACK)
  entrances.update()
  exits.update()
  if switch_draw_entrances is True:
    entrances.draw(screen)
  if switch_draw_exits is True:
    exits.draw(screen)
  pygame.display.update()
  print(collide)


pygame.quit()
