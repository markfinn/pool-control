from __future__ import division
import display
import threading
import time
import traceback
import sys
import contextlib


class Element(object):
  def refresh(self):
    self.parent.refresh()

  @property
  def center(self):
      return self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2

  @property
  def pos(self):
    return self.parent.pos

  @property
  def size(self):
    return self.parent.size

  @property
  def refreshHold(self):
    return self.parent.refreshHold


class Container(object):
  def __init__(self):
    self.children=[]

  def draw(self, draw):
    for c in self.children:
      try:
        c.draw(draw)
      except:
         traceback.print_exc(file=sys.stderr)  
    
  def add(self, c):
    self.children.append(c)
    c.parent = self


class GuiBase(object):
  def __init__(self):
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
          self._refresh(wait=True)
        except:
           traceback.print_exc(file=sys.stderr)  

  def refresh(self):
      with self.refreshcond:
        self.refreshneeded=True
        self.refreshcond.notifyAll()


  @property
  @contextlib.contextmanager
  def refreshHold(self):
    self.refreshing.acquire()
    yield self
    self.refreshing.release()






class GuiScreen(GuiBase, Container, display.Screen, Element):
  def __init__(self, spi):
    display.Screen.__init__(self, spi)
    Container.__init__(self)
    GuiBase.__init__(self)

  def _refresh(self, wait):
    display.Screen.refresh(self, wait=wait)



class GuiCurses(GuiBase, Container, Element):
  def __init__(self, win):
    global Image
    import Image
    global ImageDraw
    import ImageDraw
    global curses
    import curses
    Container.__init__(self)
    GuiBase.__init__(self)
    self.win=win
    curses.curs_set(0)

  @property
  def size(self):
    return 400, 300


  def _refresh(self, wait):
      image = Image.new('L', self.size, 255)
      draw = ImageDraw.Draw(image)
      self.draw(draw)
      print self.win.getbegyx(), self.win.getmaxyx()





class TextBox(Element):
  def __init__(self):
    self.text=''

  def draw(self, draw):
      display.textbox(draw, self.text, size=self.parent.size, center=self.parent.center, fill = 0)
    




class GroupMember(Container, Element):
  def __init__(self, g, i):
    Container.__init__(self)
    self.parent=g
    self.i=i

  @property
  def pos(self):
    return self.parent.posOf(self.i)

  @property
  def size(self):
    return self.parent.sizeOf(self.i)



class Group(Element):
  def __init__(self):
      raise NotImplemented()

  @staticmethod
  def makesizes(sizes, psize):
    t=sum(sizes)
    psize
    outsizes=[]
    for s in sizes:
      x=int(s/t*psize+.5)
      outsizes.append(x)
      psize-=x
      t-=s
    return outsizes


  def getMember(self, i):
    return self.members[i]

  def draw(self, draw):
    for m in self.members:
      try:
        m.draw(draw)
      except:
         traceback.print_exc(file=sys.stderr)

  @property
  def sizes(self):
    try:
      return self._sizes
    except AttributeError:
      self._sizes = self._calcsizes()
      return self._sizes

class HGroup(Group):
  def __init__(self, sizes):
    self.members=[GroupMember(self, i) for i in xrange(len(sizes))]
    self.rawsizes = sizes

  def _calcsizes(self):
     return self.makesizes(self.rawsizes, self.parent.size[0])

  def posOf(self, i):
    return self.pos[0]+sum(self.sizes[:i]), self.pos[1]

  def sizeOf(self, i):
    return self.sizes[i],self.size[1]


class VGroup(Group):
  def __init__(self, sizes):
    self.members=[GroupMember(self, i) for i in xrange(len(sizes))]
    self.rawsizes = sizes

  def _calcsizes(self):
     return self.makesizes(self.rawsizes, self.parent.size[1])

  def posOf(self, i):
    return self.pos[0], self.pos[1]+sum(self.sizes[:i])

  def sizeOf(self, i):
    return self.size[0],self.sizes[i]


def main():
    g=GuiScreen((1,0))
    t=TextBox()
    t.text="Hello, World!"
    g.add(t)
    t.refresh()

    time.sleep(5)

if __name__ == '__main__':
    main()
