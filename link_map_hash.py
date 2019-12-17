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
num_clicks = 0


class Marker(pygame.sprite.Sprite):

  """
used to draw the marker at a given position
  """

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.Surface((50, 50))
    self.image.fill(RED)
    self.image.set_alpha(50)

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

  def check_click(self, mouse):
    if self.rect.collidepoint(mouse):
      self.image.set_alpha(200)
    if not self.rect.collidepoint(mouse):
      self.image.set_alpha(50)


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
      new_key = key + '_entrance'
      new_key = Marker(pos_x, pos_y)
      all_sprites.add(new_key)
      self.switch = True
    else:
      key = self.key_dict[-1]
      old_pos = self.con_dict[key]
      pos_x, pos_y = position
      new_key = key + '_exit'
      new_key = Marker(pos_x, pos_y)
      all_sprites.add(new_key)
      self.con_dict[key] = [old_pos, position]
      self.switch = False

  def return_pos(self, key):
    return self.con_dict()



    #test2 = Marker(10, 10)
all_sprites = pygame.sprite.Group()
# all_sprites.add(test2)
connections = Connections()

running = True

while running:
  for s in all_sprites:
    mouse_pos = pygame.mouse.get_pos()
    s.check_click(mouse_pos)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
      mouse = pygame.mouse.get_pos()
      connections.add_entrance_or_exit(mouse)

      # print(all_sprites)

  screen.fill(BLACK)
  all_sprites.update()
  all_sprites.draw(screen)
  pygame.display.update()
  for i in connections.key_dict:
    var = connections.con_dict[i]

    print('key: ' + i + '; value: ' + str(var))


pygame.quit()
