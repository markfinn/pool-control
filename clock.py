import time
import traceback
import threading
import sys



import threading
class Clock(object):
    def __init__(self):
      self.lastreport=None

    def readLocal(self, format='%c'):
      ts = time.localtime()
      return time.strftime(format, ts)

    def _report(self, interval, format, callback):
        while True:
            if interval:
                time.sleep(interval)
            else:
                now = time.time()
                while self.lastreport and int(self.lastreport)>=int(now):
                    time.sleep(int(self.lastreport)+1-now)
                    now = time.time()
                self.lastreport=now
            v = self.readLocal(format)
            try:
                callback(v)
            except:
                traceback.print_exc(file=sys.stderr)
                
    def reportLocal(self, interval, format, callback):
        t = threading.Thread(target=self._report, args=(interval, format, callback,), name='clock_report')
        t.daemon=True
        t.start()

