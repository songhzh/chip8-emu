import time
import random
import argparse
from pathlib import Path
import pygame
from wrapper import GameWrapper

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

  game = GameWrapper(rom.file_path, pixels, sfx)

  while not game.done:
    game.handleEvents()
    game.step()

    screen.blit(pygame.transform.scale(pixels, screen.get_rect().size), (0, 0))
    pygame.display.flip()

    clock.tick(500)