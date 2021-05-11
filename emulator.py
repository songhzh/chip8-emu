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
  def __init__(self, file):
    self.file = file
    self.reset()

  def reset(self):
    self.regs = Registers()
    self.flags = Flags()
    self.stack = [0] * 16
    self.mem = bytearray(4096)
    self.gfx = [False] * 2048 # 64 * 32 bits
    self.keys = [False] * 16

    self.load_fontset()
    self.load_rom()

  def load_fontset(self):
    for i in range(80):
      self.mem[0x50+i] = fontset[i]

  def load_rom(self):
    with open(self.file, 'rb') as f:
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

  def stepInstruction(self):
    if self.flags.wait:
      return

    opcode = self.fetch()
    execute = decode(opcode)
    execute(self, opcode)

  def stepTimers(self):
    if self.flags.timer > 0:
      self.flags.timer -= 1
      return

    if self.regs.dt > 0:
      self.regs.dt -= 1
    if self.regs.st > 0:
      self.regs.st -= 1
      self.flags.sfx = self.regs.st == 0
    
    self.flags.timer = 8 # approximate 60 Hz

  def sfxFlag(self):
    flag = self.flags.sfx
    self.flags.sfx = False
    return flag

  def drawFlag(self):
    flag = self.flags.draw
    self.flags.draw = False
    return flag
    
  def updateKeys(self, pressed):
    for i, k in enumerate(pressed):
      if k and self.flags.wait:
        self.regs[self.flags.vx] = i
        self.flags.wait = False
        break
    self.keys = pressed