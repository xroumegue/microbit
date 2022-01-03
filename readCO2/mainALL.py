from microbit import display, pin0, pin14, button_a
from time import sleep
#from tm1637 import TM1637
from utime import sleep_us
_SEG=bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x40')
class TM1637:
  def __init__(self,clk,dio,bright=7):
    self.clk=clk
    self.dio=dio
    if not 0<=bright<=7:raise ValueError("Brightness out of range")
    self._bright=bright
    sleep_us(10)
    self._write_data_cmd()
    self._write_dsp_ctrl()
  def _write_digital(self,pin,state):
    pin.write_digital(state)
    sleep_us(10)
  def _start(self):
    self._write_digital(self.dio,0)
    self._write_digital(self.clk,0)
  def _stop(self):
    self._write_digital(self.dio,0)
    self._write_digital(self.clk,1)
    self._write_digital(self.dio,1)
  def _write_data_cmd(self):
    self._start()
    self._write_byte(0x40)
    self._stop()
  def _write_dsp_ctrl(self):
    self._start()
    self._write_byte(0x80|0x08|self._bright)
    self._stop()
  def _write_byte(self,b):
    for i in range(8):
      self._write_digital(self.dio,(b>>i)&1)
      self._write_digital(self.clk,1)
      self._write_digital(self.clk,0)
    self._write_digital(self.clk,0)
    self._write_digital(self.clk,1)
    self._write_digital(self.clk,0)
  def write(self,segs,pos=0):
    if not 0<=pos<=5:raise ValueError("Position out of range")
    self._write_data_cmd()
    self._start()
    self._write_byte(0xC0|pos)
    for seg in segs:self._write_byte(seg)
    self._stop()
    self._write_dsp_ctrl()
  def encode_str(self,str):
    segs=bytearray(len(str))
    for i in range(len(str)):segs[i]=self.encode_char(str[i])
    return segs
  def encode_char(self,char):
    o=ord(char)
    if o==45:return _SEG[10]
    if o>=48 and o<=57:return _SEG[o-48]
    raise ValueError("Character out of range: {:d} '{:s}'".format(o,chr(o)))

  def show(self,str,colon=False):
    segs=self.encode_str(str)
    if len(segs)>1 and colon:segs[1]|=128
    self.write(segs[:4])

#from sgp30 import SGP30
from microbit import i2c,sleep
class SGP30:
  def __init__(self):
    self.serial=self.read([0x36, 0x82],10,3)
    if self.read([0x20,0x2f],0.01,1)[0]&0xf0!=0x0020:raise RuntimeError('SGP30 Not detected')
    self.iaq_init()
  def TVOC(self):return self.iaq_measure()[1]
  def baseline_TVOC(self):return self.get_iaq_baseline()[1]
  def eCO2(self):return self.iaq_measure()[0]
  def baseline_eCO2(self):return self.get_iaq_baseline()[0]
  def iaq_init(self):self.run(['iaq_init',[0x20,0x03],0,10])
  def iaq_measure(self):return self.run(['iaq_measure',[0x20,0x08],2,50])
  def get_iaq_baseline(self):return self.run(['iaq_get_baseline',[0x20,0x15],2,10])
  def set_iaq_baseline(self,eCO2,TVOC):
    if eCO2==0 and TVOC==0:raise RuntimeError('Invalid baseline')
    b=[]
    for i in [TVOC,eCO2]:
      a=[i>>8,i&0xFF]
      a.append(self.g_crc(a))
      b+=a
    self.run(['iaq_set_baseline',[0x20,0x1e]+b,0,10])
  def set_iaq_humidity(self,PM3):
    b=[]
    for i in [int(PM3*256)]:
      a=[i>>8,i&0xFF]
      a.append(self.g_crc(a))
      b+=a
    self.run(['iaq_set_humidity',[0x20,0x61]+b,0,10])
  def run(self,profile):
    n,cmd,s,d=profile
    return self.read(cmd,d,s)
  def read(self,cmd,d,rs):
    i2c.write(0x58,bytearray(cmd))
    sleep(d)
    if not rs:return None
    cr=i2c.read(0x58,rs*3)
    o=[]
    for i in range(rs):
      w=[cr[3*i],cr[3*i+1]]
      c=cr[3*i+2]
      if self.g_crc(w)!=c:raise RuntimeError('CRC Error')
      o.append(w[0]<<8|w[1])
    return o
  def g_crc(self,data):
    c=0xFF
    for byte in data:
      c^=byte
      for _ in range(8):
        if c&0x80:c=(c<<1)^0x31
        else:c<<=1
    return c&0xFF

from struct import pack

C = SGP30()
lcd = TM1637(pin0, pin14)

display.scroll("...CO2...")
i=0
f=None

while True:
    m = C.eCO2()
    lcd.show("{:04d}".format(m))
    if m > 600:
        display.show("!", clear = True, wait = True)
    if button_a.is_pressed():
        f = open('meas.dat', 'wb')
        i = 0
    if f:
        if i < 8192:
            f.write(pack("H", m))
            i += 1
            display.show("+", clear = True, wait = False)
        else:
            f.close()
            f = None
    sleep(1)
