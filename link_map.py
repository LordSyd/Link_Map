import pygame


pygame.init()

clock = pygame.time.Clock()
clock.tick(20)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((500, 500))
running = True

connections_list = []
num_clicks = 0


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
    if self.entrance is None:
      self.entrance = position
    if self.exit is None:
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


#test2 = Marker(10, 10)
all_sprites = pygame.sprite.Group()
# all_sprites.add(test2)

running = True

while running:
  if num_clicks > 0:
    for connection in connections_list:
      if not connection.check_if_full():
        x, y = connection.get_entrance()
        marker_entrance = connection + '_entrance'
        marker_entrance = Marker(x, y)
        all_sprites.add(marker_entrance)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      num_clicks += 1
      for s in all_sprites:
        s.check_click(event.pos)
      var = get_instance_name(pygame.mouse.get_pos())
      var = Connection()
      connections_list.append(var)
      var.set_entrance_or_exit(pygame.mouse.get_pos())

      print(var.get_entrance())
      print(all_sprites)
      print(connections_list[0].get_entrance())
      s, j = var.get_entrance()
      test = Marker(s, j)
      all_sprites.add(test)

  screen.fill(BLACK)
  all_sprites.update()
  all_sprites.draw(screen)
  pygame.display.update()


pygame.quit()
