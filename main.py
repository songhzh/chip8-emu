import time
import random
import pygame
from emulator import Emulator

if __name__ == '__main__':
  random.seed()

  screen = pygame.display.set_mode((640, 320))
  pixels = pygame.Surface((64, 32))
  pygame.display.set_caption('CHIP-8 EMULATOR')
  clock = pygame.time.Clock()

  emu = Emulator()
  emu.load_rom('roms/maze.ch8')

  done = False

  while not done:
    for evt in pygame.event.get():
      if evt.type == pygame.QUIT:
        done = True
    
    emu.handleCycle()
    emu.handleDraw(pixels)
    emu.handleKeys()
    
    screen.blit(pygame.transform.scale(pixels, screen.get_rect().size), (0, 0))
    pygame.display.flip()
    clock.tick(60)