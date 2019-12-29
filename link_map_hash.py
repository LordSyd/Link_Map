import pygame


pygame.init()

clock = pygame.time.Clock()
clock.tick(20)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((500, 500))
running = True


LEFT = 1


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
      all_sprites.add(new_key)
      self.switch = True
    else:
      key = self.key_dict[-1]
      old_pos = self.con_dict[key]
      pos_x, pos_y = position
      new_key = key + "_exit"
      new_key = Marker(pos_x, pos_y, key, "exit")
      all_sprites.add(new_key)
      self.con_dict[key] = [old_pos, position]
      self.switch = False

  def return_pos_pair(self, key):
    return self.con_dict[key]


all_sprites = pygame.sprite.Group()

connections = Connections()


def check_collision(pos):
  collide = False
  for s in all_sprites:
    if s.check_click(pos) == True:
      collide = True
      return collide
  return collide


running = True


while running:

  mouse = pygame.mouse.get_pos()
  collide = check_collision(mouse)

  # for s in all_sprites:
  # s.check_click(mouse)
  #collide = s.collide_check(mouse)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
      if collide == False or collide == None:
        mouse = pygame.mouse.get_pos()
        connections.add_entrance_or_exit(mouse)

  screen.fill(BLACK)
  all_sprites.update()
  all_sprites.draw(screen)
  pygame.display.update()
  print(collide)

  # print(s.get_function())
  # for i in connections.key_dict:
  #var = connections.con_dict[i]

  #print('key: ' + i + '; value: ' + str(var))


pygame.quit()
