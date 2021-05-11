import pygame
from emulator import Emulator

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame_keys = [
  pygame.K_x, # 0
  pygame.K_1, # 1
  pygame.K_2, # 2
  pygame.K_3, # 3
  pygame.K_q, # 4
  pygame.K_w, # 5
  pygame.K_e, # 6
  pygame.K_a, # 7
  pygame.K_s, # 8
  pygame.K_d, # 9
  pygame.K_z, # A
  pygame.K_c, # B
  pygame.K_4, # C
  pygame.K_r, # D
  pygame.K_f, # E
  pygame.K_v  # F
]

class GameWrapper:
  def __init__(self, rom, pixels, sfx):
    self.emu = Emulator(rom)
    self.pixels = pixels
    self.sfx = sfx
    
    self.done = False
    self.paused = False

  def handleEvents(self):
    for evt in pygame.event.get():
      if evt.type == pygame.QUIT:
          self.done = True
      if evt.type == pygame.KEYDOWN:
        if evt.key == pygame.K_ESCAPE:
          self.paused = not self.paused
        if evt.key == pygame.K_BACKSPACE:
          self.emu.reset()
  
  def handleSfx(self):
    if not self.emu.sfxFlag():
      return
    
    self.sfx.play()
  
  def handleDraw(self):
    if not self.emu.drawFlag():
      return

    self.pixels.fill(BLACK)

    for y in  range(32):
      for x in range(64):
        if self.emu.gfx[y*64+x]:
          self.pixels.set_at((x, y), WHITE)

  def handleKeys(self):
    inputs = pygame.key.get_pressed()
    pressed = [inputs[k] for k in pygame_keys]
    self.emu.updateKeys(pressed)

  def step(self):
    if self.paused:
      return

    self.emu.stepInstruction()
    self.emu.stepTimers() # should step at 60 Hz but oh well

    self.handleSfx()
    self.handleDraw()
    self.handleKeys()