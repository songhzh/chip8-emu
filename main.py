import time
import random
import argparse
from pathlib import Path
import pygame
from emulator import Emulator

if __name__ == '__main__':
  random.seed()
  
  parser = argparse.ArgumentParser()
  parser.add_argument('file_path', type=Path)
  rom = parser.parse_args()

  if not rom.file_path.exists():
    quit('Rom not found')

  screen = pygame.display.set_mode((640, 320))
  pixels = pygame.Surface((64, 32))
  pygame.display.set_caption('CHIP-8 EMULATOR')
  pygame.mixer.init()
  sfx = pygame.mixer.Sound('sfx/blip.wav')
  clock = pygame.time.Clock()

  emu = Emulator(rom.file_path)

  done = False
  paused = False

  while not done:
    pressed = pygame.key.get_pressed()

    for evt in pygame.event.get():
      if evt.type == pygame.QUIT:
        done = True
      if evt.type == pygame.KEYDOWN:
        if evt.key == pygame.K_ESCAPE:
          paused = not paused
        if evt.key == pygame.K_BACKSPACE:
          emu.reset()

    if not paused:
      emu.handleCycle(sfx)
      emu.handleDraw(pixels)
      emu.handleKeys(pressed)
      
      screen.blit(pygame.transform.scale(pixels, screen.get_rect().size), (0, 0))
      pygame.display.flip()

    clock.tick(500)