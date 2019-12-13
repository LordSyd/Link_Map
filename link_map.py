import pygame


pygame.init()

clock = pygame.time.Clock()
clock.tick(20)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((500, 500))

connections_list = []
num_clicks = 1


def get_instance_name(position):
  """
generates a name string for a clicked positon to be used for instantiating Connection()
  """
  position_x, position_y = position
  instance_name = str(position_x) + str(position_y)
  return instance_name


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
      return True
    if not self.rect.collidepoint(mouse):
      self.image.set_alpha(50)

  def get_sprite_position(self):
    return (self.rect.x, self.rect.y)


class Connection:
  """
  used as a container for an entrance/exit-pair, self.set_entrance_or_exit(position) 
  is used to assign clicked coordinates
  """

  def __init__(self, full=False):
    self.entrance = None
    self.exit = None
    self.full = full

  def set_entrance_or_exit(self, position):
    if self.check_if_full():
      print('full')
      return
    elif self.entrance is None:
      self.entrance = position
    elif not self.entrance is None and self.exit is None:
      self.exit = position
      self.full = True

  def get_entrance(self):
    if self.entrance is None:
      return
    else:
      return self.entrance

  def get_exit(self):
    if self.exit is None:
      return
    else:
      return self.exit

  def check_if_full(self):
    return self.full


all_sprites = pygame.sprite.Group()


running = True

while running:
  if num_clicks > 0:
    for s in all_sprites:
      mouse_pos = pygame.mouse.get_pos()
      s.check_click(mouse_pos)
      # print(type(s))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      num_clicks += 1
      var = get_instance_name(pygame.mouse.get_pos())
      var = Connection()
      # connections_list.append(var)
      var.set_entrance_or_exit(pygame.mouse.get_pos())

      print(var.get_exit())
      print(var.get_entrance())
      # print(all_sprites)
      # print(connections_list[0].get_entrance())
      s, j = var.get_entrance()  # gets mouse position
      test = Marker(s, j)
      all_sprites.add(test)

  screen.fill(BLACK)
  all_sprites.update()
  all_sprites.draw(screen)
  pygame.display.update()


pygame.quit()
