import pygame
from registers import Registers
from flags import Flags
from opcodes import decode

fontset = [
  0xf0, 0x90, 0x90, 0x90, 0xf0, # 0
  0x20, 0x60, 0x20, 0x20, 0x70, # 1
  0xf0, 0x10, 0xf0, 0x80, 0xf0, # 2
  0xf0, 0x10, 0xf0, 0x10, 0xf0, # 3
  0x90, 0x90, 0xf0, 0x10, 0x10, # 4
  0xf0, 0x80, 0xf0, 0x10, 0xf0, # 5
  0xf0, 0x80, 0xf0, 0x90, 0xf0, # 6
  0xf0, 0x10, 0x20, 0x40, 0x40, # 7
  0xf0, 0x90, 0xf0, 0x90, 0xf0, # 8
  0xf0, 0x90, 0xf0, 0x10, 0xf0, # 9
  0xf0, 0x90, 0xf0, 0x90, 0x90, # A
  0xe0, 0x90, 0xe0, 0x90, 0xe0, # B
  0xf0, 0x80, 0x80, 0x80, 0xf0, # C
  0xe0, 0x90, 0x90, 0x90, 0xe0, # D
  0xf0, 0x80, 0xf0, 0x80, 0xf0, # E
  0xf0, 0x80, 0xf0, 0x80, 0x80  # F
]

keys = [
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

class Emulator:
  def __init__(self):
    self.regs = Registers()
    self.flags = Flags()
    self.stack = [0] * 16
    self.mem = bytearray(4096)
    self.gfx = [False] * 2048 # 64 * 32 bits
    self.keys = [False] * 16

    self.load_fontset()

  def load_fontset(self):
    for i in range(80):
      self.mem[0x50+i] = fontset[i]

  def load_rom(self, file):
    with open(file, 'rb') as f:
      i = 0
      byte = f.read(1)
      while byte != b'':
        self.mem[0x200+i] = int.from_bytes(byte, byteorder='big', signed=False)
        i += 1
        byte = f.read(1)

  def fetch(self):
    lo = self.mem[self.regs.pc]
    self.regs.pc += 1
    hi = self.mem[self.regs.pc]
    self.regs.pc += 1
    return (lo << 8) | hi

  def handleCycle(self, sfx):
    if self.flags.wait:
      return

    opcode = self.fetch()
    execute = decode(opcode)
    execute(self, opcode)

    if self.regs.dt > 0:
      self.regs.dt -= 1
    if self.regs.st > 0:
      self.regs.st -= 1
      if self.regs.st == 0:
        sfx.play()

  def handleDraw(self, pixels):
    if not self.flags.draw:
      return

    pixels.fill((0, 0, 0))

    for y in  range(32):
      for x in range(64):
        if self.gfx[y*64+x]:
          pixels.set_at((x, y), (255, 255, 255))

    self.flags.draw = False
  
  def handleKeys(self, pressed):
    self.keys = [False] * 16

    for i, k in enumerate(keys):
      if pressed[k]:
        self.keys[i] = True
        self.flags.wait = False
