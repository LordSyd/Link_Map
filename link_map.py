import pygame


pygame.init()

clock = pygame.time.Clock()
clock.tick(20)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((500, 500))
running = True

connections_key_list = []
num_clicks = 0

LEFT = 1


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
    if not self.rect.collidepoint(mouse):
      self.image.set_alpha(50)


class ConnectionHashMap:
  def __init__(self, array_size):
    self.array_size = array_size
    self.array = [None for item in range(array_size)]

  def hash(self, key, count_collisions=0):
    key_bytes = key.encode()
    hash_code = sum(key_bytes)
    return hash_code + count_collisions

  def compressor(self, hash_code):
    return hash_code % self.array_size

  def assign(self, key, value):
    array_index = self.compressor(self.hash(key))
    current_array_value = self.array[array_index]

    if current_array_value is None:
      self.array[array_index] = [key, value]
      return

    if current_array_value[0] == key:
      self.array[array_index] = [key, value]
      return

    # Collision!

    number_collisions = 1

    while(current_array_value[0] != key):
      new_hash_code = self.hash(key, number_collisions)
      new_array_index = self.compressor(new_hash_code)
      current_array_value = self.array[new_array_index]

      if current_array_value is None:
        self.array[new_array_index] = [key, value]
        return

      if current_array_value[0] == key:
        self.array[new_array_index] = [key, value]
        return

      number_collisions += 1

    return

  def retrieve(self, key):
    array_index = self.compressor(self.hash(key))
    possible_return_value = self.array[array_index]

    if possible_return_value is None:
      return None

    if possible_return_value[0] == key:
      return possible_return_value[1]

    retrieval_collisions = 1

    while (possible_return_value != key):
      new_hash_code = self.hash(key, retrieval_collisions)
      retrieving_array_index = self.compressor(new_hash_code)
      possible_return_value = self.array[retrieving_array_index]

      if possible_return_value is None:
        return None

      if possible_return_value[0] == key:
        return possible_return_value[1]

      retrieval_collisions += 1

    return


connections = ConnectionHashMap(200)

#test2 = Marker(10, 10)
all_sprites = pygame.sprite.Group()
# all_sprites.add(test2)

running = True

while running:
  if num_clicks > 0:
    for s in all_sprites:
      mouse_pos = pygame.mouse.get_pos()
      s.check_click(mouse_pos)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
      mouse = pygame.mouse.get_pos()
      num_clicks += 1
      if num_clicks % 3 == 1:
        var = get_instance_name(mouse)
        connections_key_list.append(var)
        connections.assign(connections_key_list[-1], mouse)
      elif num_clicks % 3 == 2:
        old_pos = connections.retrieve(connections_key_list[-1])
        connections.assign(connections_key_list[-1], (old_pos, mouse))

      # print(all_sprites)

  screen.fill(BLACK)
  all_sprites.update()
  all_sprites.draw(screen)
  pygame.display.update()
  print((num_clicks % 3))
  for i in connections_key_list:
    var = connections.retrieve(i)

    print('key: ' + i + '; value: ' + str(var))


pygame.quit()
