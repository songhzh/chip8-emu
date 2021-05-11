import random

def read(word, mask):
  val = word & mask
  if mask & 0x000f:
    return val
  if mask & 0x00f0:
    return val >> 4
  if mask & 0x0f00:
    return val >> 8
  if mask & 0xf000:
    return val >> 12
  raise ValueError('Invalid mask', mask)

def _0NNN(emu, word):
  # sys addr, opcode ignored
  pass

def _00E0(emu, word):
  # cls
  emu.gfx = [False] * 2048
  emu.flags.draw = True

def _00EE(emu, word):
  # ret
  emu.regs.sp -= 1
  emu.regs.pc = emu.stack[emu.regs.sp]

def _1NNN(emu, word):
  # jp NNN
  nnn = read(word, 0x0fff)
  emu.regs.pc = nnn

def _2NNN(emu, word):
  # call NNN
  nnn = read(word, 0x0fff)
  emu.stack[emu.regs.sp] = emu.regs.pc
  emu.regs.sp += 1
  emu.regs.pc = nnn

def _3XNN(emu, word):
  # skip if vx == nn
  vx = read(word, 0x0f00)
  nn = read(word, 0x00ff)
  if emu.regs[vx] == nn:
    emu.regs.pc += 2

def _4XNN(emu, word):
  # skip if vx != nn
  vx = read(word, 0x0f00)
  nn = read(word, 0x00ff)
  if emu.regs[vx] != nn:
    emu.regs.pc += 2

def _5XY0(emu, word):
  # skip if vx == vy
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  if emu.regs[vx] == emu.regs[vy]:
    emu.regs.pc += 2

def _6XNN(emu, word):
  # vx = nn
  vx = read(word, 0x0f00)
  nn = read(word, 0x00ff)
  emu.regs[vx] = nn

def _7XNN(emu, word):
  # vx = vx + nn
  vx = read(word, 0x0f00)
  nn = read(word, 0x00ff)
  emu.regs[vx] += nn

def _8XY0(emu, word):
  # vx = vy
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  emu.regs[vx] = emu.regs[vy]

def _8XY1(emu, word):
  # vx = vx OR vy
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  emu.regs[vx] |= emu.regs[vy]

def _8XY2(emu, word):
  # vx = vx AND vy
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  emu.regs[vx] &= emu.regs[vy]

def _8XY3(emu, word):
  # vx = vx XOR vy
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  emu.regs[vx] ^= emu.regs[vy]

def _8XY4(emu, word):
  # vx = vx + vy, vf = CARRY
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  carry = 1 if emu.regs[vx] + emu.regs[vy] > 0xff else 0
  emu.regs[0xf] = carry
  emu.regs[vx] += emu.regs[vy]

def _8XY5(emu, word):
  # vx = vx - vy, vf = NOT BORROW
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  not_borrow = 1 if emu.regs[vx] > emu.regs[vy] else 0
  emu.regs[0xf] = not_borrow
  emu.regs[vx] -= emu.regs[vy]

def _8XY6(emu, word):
  # vx = vx >> 1, vf = LSB
  vx = read(word, 0x0f00)
  lsb = emu.regs[vx] & 1
  emu.regs[0xf] = lsb
  emu.regs[vx] >>= 1

def _8XY7(emu, word):
  # vx = vy - vx, vf = NOT BORROW
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  not_borrow = 1 if emu.regs[vy] > emu.regs[vx] else 0
  emu.regs[0xf] = not_borrow
  emu.regs[vx] = emu.regs[vy] - emu.regs[vx]

def _8XYE(emu, word):
  # vx = vx << 1, vf = MSB
  vx = read(word, 0x0f00)
  msb = 1 if emu.regs[vx] & 0x80 else 0
  emu.regs[0xf] = msb
  emu.regs[vx] <<= 1

def _9XY0(emu, word):
  # skip if vx != vy
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  if emu.regs[vx] != emu.regs[vy]:
    emu.regs.pc += 2

def _ANNN(emu, word):
  # i = nnn
  nnn = read(word, 0x0fff)
  emu.regs.i = nnn

def _BNNN(emu, word):
  # jp nnn + v0
  nnn = read(word, 0x0fff)
  emu.regs.pc = nnn + emu.regs[0x0]

def _CXNN(emu, word):
  vx = read(word, 0x0f00)
  nn = read(word, 0x00ff)
  rand = random.randint(0x00, 0xff)
  emu.regs[vx] = rand & nn

def _DXYN(emu, word):
  # draw sprite
  vx = read(word, 0x0f00)
  vy = read(word, 0x00f0)
  n = read(word, 0x000f)
  x = emu.regs[vx]
  y = emu.regs[vy]
  emu.regs[0xf] = 0
  for i in range(n):
    line = emu.mem[emu.regs.i+i]
    for j in range(8):
      px = True if line & (0x80 >> j) else False
      x_coord = (x + j) % 64
      y_coord = (y + i) % 32
      g = y_coord * 64 + x_coord
      if emu.gfx[g] and px:
        emu.regs[0xf] = 1
      emu.gfx[g] ^= px
  emu.flags.draw = True

def _EX9E(emu, word):
  # skip if key in vx is pressed
  vx = read(word, 0x0f00)
  if emu.keys[emu.regs[vx]]:
    emu.regs.pc += 2

def _EXA1(emu, word):
  # skip if key in vx is not pressed
  vx = read(word, 0x0f00)
  if not emu.keys[emu.regs[vx]]:
    emu.regs.pc += 2

def _FX07(emu, word):
  # vx = dt
  vx = read(word, 0x0f00)
  emu.regs[vx] = emu.regs.dt

def _FX0A(emu, word):
  # wait for keypress and store in vx
  vx = read(word, 0x0f00)
  emu.flags.wait = True
  emu.flags.vx = vx

def _FX15(emu, word):
  # dt = vx
  vx = read(word, 0x0f00)
  emu.regs.dt = emu.regs[vx]

def _FX18(emu, word):
  # st = vx
  vx = read(word, 0x0f00)
  emu.regs.st = emu.regs[vx]

def _FX1E(emu, word):
  # i = i + vx
  vx = read(word, 0x0f00)
  emu.regs.i += emu.regs[vx]

def _FX29(emu, word):
  # i = sprite location for vx
  vx = read(word, 0x0f00)
  emu.regs.i = 0x50 + emu.regs[vx] * 5

def _FX33(emu, word):
  # i, i+1, i+2 = bcd vx
  vx = read(word, 0x0f00)
  val = emu.regs[vx]
  i = emu.regs.i
  emu.mem[i] = val // 100
  emu.mem[i+1] = val % 100 // 10
  emu.mem[i+2] = val % 10

def _FX55(emu, word):
  # store v0 to vx inclusive starting at i
  vx = read(word, 0x0f00)
  for r in range(vx+1):
    emu.mem[emu.regs.i+r] = emu.regs[r]

def _FX65(emu, word):
  # read v0 to vx inclusive starting at i
  vx = read(word, 0x0f00)
  for r in range(vx+1):
    emu.regs[r] = emu.mem[emu.regs.i+r]

opcodes = [
  lambda word: decode_0(word),
  lambda _: _1NNN,
  lambda _: _2NNN,
  lambda _: _3XNN,
  lambda _: _4XNN,
  lambda _: _5XY0,
  lambda _: _6XNN,
  lambda _: _7XNN,
  lambda word: decode_8(word),
  lambda _: _9XY0,
  lambda _: _ANNN,
  lambda _: _BNNN,
  lambda _: _CXNN,
  lambda _: _DXYN,
  lambda word: decode_e(word),
  lambda word: decode_f(word),
]

opcodes_0 = {
  0x0e0: _00E0,
  0x0ee: _00EE
}

opcodes_8 = {
  0x0: _8XY0,
  0x1: _8XY1,
  0x2: _8XY2,
  0x3: _8XY3,
  0x4: _8XY4,
  0x5: _8XY5,
  0x6: _8XY6,
  0x7: _8XY7,
  0xe: _8XYE
}

opcodes_e = {
  0x9e: _EX9E,
  0xa1: _EXA1
}

opcodes_f = {
  0x07: _FX07,
  0x0A: _FX0A,
  0x15: _FX15,
  0x18: _FX18,
  0x1E: _FX1E,
  0x29: _FX29,
  0x33: _FX33,
  0x55: _FX55,
  0x65: _FX65
}

def decode(word):
  prefix = (word & 0xf000) >> 12
  return opcodes[prefix](word)

def decode_0(word):
  suffix = word & 0xfff
  return opcodes_0.get(suffix, _0NNN)

def decode_8(word):
  suffix = word & 0xf
  return opcodes_8.get(suffix)

def decode_e(word):
  suffix = word & 0xff
  return opcodes_e.get(suffix)

def decode_f(word):
  suffix = word & 0xff
  return opcodes_f.get(suffix)