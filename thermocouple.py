import time
import traceback
import threading
import sys

class max6675(object):
    def __init__(self, spi):
        if spi==None:#dummy, not on rpi
            self.spi=None
        else:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(spi[0], spi[1])
        self.lastread = None

    def read(self, wait=False):

        now = time.time()
        if wait:
            while self.lastread != None and self.lastread + .33 > now:
              time.sleep(self.lastread+.33 - now)
              now = time.time()

        
        if self.lastread == None or self.lastread + .33 <= now:
            if self.spi==None:#dummy
                self.temp = 20.0
                return self.temp
    
            self.spi.max_speed_hz = 2000000
            self.spi.mode = 0b01


            v = self.spi.readbytes(2)
            self.lastread = time.time()

            v = (v[0]<<8)|v[1]
            temp = (v>>3)/4.0
            opentherm = (v>>2)&1

            self.temp=temp

        return self.temp



    def _report(self, callback):
        while True:
            v = self.read(True)
            try:
                callback(v)
            except:
                traceback.print_exc(file=sys.stderr)
                
    def report(self, callback):
        t = threading.Thread(target=self._report, args=(callback,), name='max6675_report')
        t.daemon=True
        t.start()

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
