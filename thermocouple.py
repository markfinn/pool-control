import spidev
import time


class max6675(object):
    def __init__(self, bus, cs):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, cs)
        self.lastread = None

    def read(self, wait=False):

        now = time.time()
        if wait:
            while self.lastread != None and self.lastread + .33 >= now:
              now = time.time()

        
        if self.lastread == None or self.lastread + .33 < now:
    
            self.spi.max_speed_hz = 2000000
            self.spi.mode = 0b01

            v = self.spi.readbytes(2)
            self.lastread = time.time()

            v = (v[0]<<8)|v[1]
            temp = (v>>3)/4.0
            opentherm = (v>>2)&1

            self.temp=temp

        return self.temp


if __name__ == '__main__':

  s = max6675(1,1)
  va=0
  v=None
  while True:
    nv = s.read(True)
    va=nv+.1*.9*va
    print nv
#    if nv!=v:
#        print nv
#    v=nv
