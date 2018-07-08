
import display
import thermocouple
import threading
import time
import traceback
import sys

class GuiScreen(display.Screen):
  def __init__(self, spi):
    super(GuiScreen, self).__init__(spi)
    self.children=[]
    self.refreshneeded=False
    self.refreshcond = threading.Condition()
    self.refreshing = threading.RLock()
    self.thread = threading.Thread(target=self._run, name='GuiScreen_refresh')
    self.thread.daemon=True
    self.thread.start()

  @property
  def pos(self):
    return 0,0
    
  def _run(self):
    while True:
      with self.refreshcond:
        while not self.refreshneeded:
          self.refreshcond.wait()
        self.refreshneeded=False
      with self.refreshing: 
        try:
          super(GuiScreen, self).refresh(wait=True)
        except:
           traceback.print_exc(file=sys.stderr)  

  def refresh(self):
      with self.refreshcond:
        self.refreshneeded=True
        self.refreshcond.notifyAll()

  def draw(self, draw):
    for c in self.children:
      try:
        c.draw(draw)
      except:
         traceback.print_exc(file=sys.stderr)  
    
  def add(self, c):
    self.children.append(c)
    c.parent = self

class Element(object):
  def refresh(self):
    self.parent.refresh()


class TextBox(Element):
  def __init__(self):
    self.text=''

  def draw(self, draw):
      display.textbox(draw, self.text, size=self.parent.size, corner=self.parent.pos, fill = 0)
    


  

def main():
    g=GuiScreen((1,0))
    t=TextBox()
    def cb(temp):
      t.text='%2.1f'%(temp*9.0/5.0+32)
      t.refresh()
    ts = thermocouple.max6675(0,0)
    ts.report(cb)
    g.add(t)
    
    while True:
      try:
        time.sleep(100)
      except KeyboardInterrupt:
        break

if __name__ == '__main__':
    main()
