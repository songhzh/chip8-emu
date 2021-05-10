import random

def read_0f00(word):
  return (word & 0x0f00) >> 8

def read_00f0(word):
  return (word & 0x00f0) >> 4

def read_0fff(word):
  return word & 0x0fff

def read_00ff(word):
  return word & 0x00ff

def _0NNN(emu, word):
  # sys addr
  # Ignored
  pass

def _00E0(emu, word):
  # cls
  pass

def _00EE(emu, word):
  # ret
  emu.sp -= 1
  emu.pc = emu.stack[emu.sp]

def _1NNN(emu, word):
  # jp NNN
  nnn = read_0fff(word)
  emu.pc = nnn

def _2NNN(emu, word):
  # call NNN
  nnn = read_0fff(word)
  emu.stack[emu.sp] = emu.pc
  emu.sp += 1
  emu.pc = nnn

def _3XNN(emu, word):
  # skip if vx == nn
  vx = read_0f00(word)
  nn = read_00ff(word)
  if emu.regs[vx] == nn:
    emu.pc += 2

def _4XNN(emu, word):
  # skip if vx != nn
  vx = read_0f00(word)
  nn = read_00ff(word)
  if emu.regs[vx] != nn:
    emu.pc += 2

def _5XY0(emu, word):
  # skip if vx == vy
  vx = read_0f00(word)
  vy = read_00f0(word)
  if emu.regs[vx] == emu.regs[vy]:
    emu.pc += 2

def _6XNN(emu, word):
  # vx = nn
  vx = read_0f00(word)
  nn = read_00ff(word)
  emu.regs[vx] = nn

def _7XNN(emu, word):
  # vx = vx + nn
  vx = read_0f00(word)
  nn = read_00f0(word)
  emu.regs[vx] += nn

def _8XY0(emu, word):
  # vx = vy
  vx = read_0f00(word)
  vy = read_00f0(word)
  emu.regs[vx] = emu.regs[vy]

def _8XY1(emu, word):
  # vx = vx OR vy
  vx = read_0f00(word)
  vy = read_00f0(word)
  emu.regs[vx] |= emu.regs[vy]

def _8XY2(emu, word):
  # vx = vx AND vy
  vx = read_0f00(word)
  vy = read_00f0(word)
  emu.regs[vx] &= emu.regs[vy]

def _8XY3(emu, word):
  # vx = vx XOR vy
  vx = read_0f00(word)
  vy = read_00f0(word)
  emu.regs[vx] ^= emu.regs[vy]

def _8XY4(emu, word):
  # vx = vx + vy, vf = CARRY
  vx = read_0f00(word)
  vy = read_00f0(word)
  res = emu.regs[vx] + emu.regs[vy]
  carry = 1 if res > 0xff else 0
  emu.regs[0xf] = carry
  emu.regs[vx] = res

def _8XY5(emu, word):
  # vx = vx - vy, vf = NOT BORROW
  vx = read_0f00(word)
  vy = read_00f0(word)
  res = emu.regs[vx] - emu.regs[vy]
  borrow = 0 if res > 0 else 1
  emu.regs[0xf] = borrow
  emu.regs[vx] = res

def _8XY6(emu, word):
  # vx = vy >> 1, vf = LSB
  vx = read_0f00(word)
  vy = read_00f0(word)
  res = emu.regs[vy] >> 1
  emu.regs[0xf] = emu.regs[vy] & 1
  emu.regs[vx] = res

def _8XY7(emu, word):
  # vx = vy - vx, vf = NOT BORROW
  vx = read_0f00(word)
  vy = read_00f0(word)
  res = emu.regs[vy] - emu.regs[vx]
  borrow = 0 if res > 0 else 1
  emu.regs[0xf] = borrow
  emu.regs[vx] = res

def _8XYE(emu, word):
  # vx = vy << 1, vf = MSB
  vx = read_0f00(word)
  vy = read_00f0(word)
  res = emu.regs[vy] << 1
  emu.regs[0xf] = emu.regs[vy] & 0x8000
  emu.regs[vx] = res

def _9XY0(emu, word):
  # skip if vx != vy
  vx = read_0f00(word)
  vy = read_00f0(word)
  if emu.regs[vx] != emu.regs[vy]:
    emu.pc += 2

def _ANNN(emu, word):
  # i = nnn
  nnn = read_0fff(word)
  emu.regs.i = nnn

def _BNNN(emu, word):
  # jp nnn + v0
  nnn = read_0fff(word)
  emu.pc = nnn + emu.regs[0x0]

def _CXNN(emu, word):
  vx = read_0f00(word)
  nn = read_00ff(word)
  rand = random.randint(0x00, 0xff)
  emu.regs[vx] = rand & nn

def _DXYN(emu, word):
  # draw sprite
  pass

def _EX9E(emu, word):
  # skip if key in vx is pressed
  pass

def _EXA1(emu, word):
  # skip if key in vx is not pressed
  pass

def _FX07(emu, word):
  # vx = dt
  vx = read_0f00(word)
  emu.regs[vx] = emu.dt

def _FX0A(emu, word):
  # wait for keypress and store in vx
  pass

def _FX15(emu, word):
  # dt = vx
  vx = read_0f00(word)
  emu.dt = emu.regs[vx]

def _FX18(emu, word):
  # st = vx
  vx = read_0f00(word)
  emu.st = emu.regs[vx]

def _FX1E(emu, word):
  # i = i + vx
  vx = read_0f00(word)
  emu.i += emu.regs[vx]

def _FX29(emu, word):
  # i = sprite location for vx
  pass

def _FX33(emu, word):
  # i, i+1, i+2 = bcd vx
  vx = read_0f00(word)
  emu.mem[emu.i] = vx // 100
  emu.mem[emu.i+1] = vx % 100 // 10
  emu.mem[emu.i+2] = vx % 10

def _FX55(emu, word):
  # store v0 to vx inclusive starting at i
  vx = read_0f00(word)
  for r in range(vx+1):
    emu.mem[emu.i] = emu.regs[r]
    emu.i += 1

def _FX65(emu, word):
  # read v0 to vx inclusive starting at i
  vx = read_0f00(word)
  for r in range(vx+1):
    emu.regs[r] = emu.mem[emu.i]
    emu.i += 1

def get_opcode(word):
  prefix = (word & 0xf000) >> 12
  if prefix == 0x0:
    suffix = word & 0xfff
    if suffix == 0x0e0:
      return _00E0
    if suffix == 0x0ee:
      return _00EE
    return _0NNN
  if prefix == 0x1:
    return _1NNN
  if prefix == 0x2:
    return _2NNN
  if prefix == 0x3:
    return _3XNN
  if prefix == 0x4:
    return _4XNN
  if prefix == 0x5:
    return _5XY0
  if prefix == 0x6:
    return _6XNN
  if prefix == 0x7:
    return _7XNN
  if prefix == 0x8:
    suffix = word & 0xf
    if suffix == 0x0:
      return _8XY0
    if suffix == 0x1:
      return _8XY1
    if suffix == 0x2:
      return _8XY2
    if suffix == 0x3:
      return _8XY3
    if suffix == 0x4:
      return _8XY4
    if suffix == 0x5:
      return _8XY5
    if suffix == 0x6:
      return _8XY6
    if suffix == 0x7:
      return _8XY7
    if suffix == 0xe:
      return _8XYE
  if prefix == 0x9:
    return _9XY0
  if prefix == 0xa:
    return _ANNN
  if prefix == 0xb:
    return _BNNN
  if prefix == 0xc:
    return _CXNN
  if prefix == 0xd:
    return _DXYN
  if prefix == 0xe:
    suffix = word & 0xff
    if suffix == 0x9e:
      return _EX9E
    if suffix == 0xa1:
      return _EXA1
  if prefix == 0xf:
    suffix = word & 0xff
    if suffix == 0x07:
      return _FX07
    if suffix == 0x0a:
      return _FX0A
    if suffix == 0x15:
      return _FX15
    if suffix == 0x18:
      return _FX18
    if suffix == 0x1e:
      return _FX1E
    if suffix == 0x29:
      return _FX29
    if suffix == 0x33:
      return _FX33
    if suffix == 0x55:
      return _FX55
    if suffix == 0x65:
      return _FX65
  raise ValueError('Invalid opcode', word)