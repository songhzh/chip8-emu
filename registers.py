class Registers:
  def __init__(self):
    self._data = bytearray(16)

    self._i = 0

    self._pc = 0x200
    self._sp = 0

    self._dt = 0
    self._st = 0

  def __getitem__(self, idx):
    return self._data[idx]

  def __setitem__(self, idx, val):
    self._data[idx] = val & 0xff

  @property
  def i(self):
    return self._i
  
  @property
  def pc(self):
    return self._pc

  @property
  def sp(self):
    return self._sp

  @property
  def dt(self):
    return self._dt

  @property
  def st(self):
    return self._st

  @i.setter
  def i(self, val):
    self._i = val & 0xfff

  @pc.setter
  def pc(self, val):
    self._pc = val & 0xfff

  @sp.setter
  def sp(self, val):
    self._sp = val & 0xfff

  @dt.setter
  def dt(self, val):
    self._dt = val & 0xff

  @st.setter
  def st(self, val):
    self._st = val & 0xff