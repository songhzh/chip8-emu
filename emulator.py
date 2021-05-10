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

  def handleCycle(self):
    if self.flags.wait:
      return

    opcode = self.fetch()
    execute = decode(opcode)
    # print(execute.__name__)
    execute(self, opcode)

    self.regs.dt -= 1
    self.regs.st -= 1

  def handleDraw(self, screen):
    if not self.flags.draw:
      return

    screen.fill((0, 0, 0))

    for y in  range(32):
      for x in range(64):
        if self.gfx[y*64+x]:
          screen.set_at((x, y), (255, 255, 255))

    self.flags.draw = False
  
  def handleKeys(self):
    self.flags.wait = False