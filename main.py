
import gui
import thermocouple
import time


def main():
    g=gui.GuiScreen((1,0))
#    g=gui.GuiScreen(None)


    with g.refreshHold:
      vg = VGroup([1, 2, 8, 2])
      g.add(vg)
    
      statusbar = HGroup([1]*10)
      vg.getMember[0].add(statusbar)
    
      tabs = HGroup([1]*10)
      vg.getMember[1].add(tabs)

      mainbox = vg.getMember[2]

      keylabels = HGroup([1]*4)
      vg.getMember[3].add(keylabels)

      t=gui.TextBox()
      def cb(temp):
        t.text='%2.1f'%(temp*9.0/5.0+32)
        t.refresh()
      ts = thermocouple.max6675((0,0))
#      ts = thermocouple.max6675(None)
      ts.report(cb)
      statusbar.getMember[0].add(t)


    
    while True:
      try:
        time.sleep(100)
      except KeyboardInterrupt:
        break

if __name__ == '__main__':
    main()



def main():
    g=GuiScreen((1,0))
    
    with g.refreshHold:
      vg = VGroup([1, 2, 8, 2])
      g.add(vg)
    
      statusbar = HGroup([1]*10)
      vg.getMember[0].add(statusbar)
    
      tabs = HGroup([1]*10)
      vg.getMember[1].add(tabs)

      mainbox = vg.getMember[2]

      keylabels = HGroup([1]*4)
      vg.getMember[3].add(keylabels)

      t=TextBox()
      t.text="Hello, World!"
      g.add(t)



    t.refresh()

    time.sleep(5)

if __name__ == '__main__':
    main()
