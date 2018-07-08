from __future__ import division
import display
import threading
import time
import traceback
import sys


class Element(object):
  def refresh(self):
    self.parent.refresh()

  @property
  def center(self):
      return self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2


class GuiScreen(display.Screen, Element):
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






class TextBox(Element):
  def __init__(self):
    self.text=''

  def draw(self, draw):
      display.textbox(draw, self.text, size=self.parent.size, center=self.parent.center, fill = 0)
    

class Hgroup(Element):
  def __init__(self, sizes):
    t=sum(sizes)
    p=self.parent.size[0]
    self.sizes=[]
    for s in sizes:
      x=int(s/t*p+.5)
      self.sizes.append(x)
      p-=x
      t-=s

  def draw(self, draw):
      display.textbox(draw, self.text, size=self.parent.size, center=self.parent.center, fill = 0)
    




  

def main():
    g=GuiScreen((1,0))
    t=TextBox()
    t.text="Hello, World!"
    g.add(t)
    t.refresh()

    time.sleep(5)

if __name__ == '__main__':
    main()
