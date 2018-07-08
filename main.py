
import gui
import thermocouple
import clock
import time


def main():
    g=gui.GuiScreen((1,0))
#    g=gui.GuiScreen(None)


    with g.refreshHold:
      vg = gui.VGroup([1, 2, 8, 2])
      g.add(vg)
    
      statusbar = gui.HGroup([4,4,1,1,1,6])
      vg.getMember(0).add(statusbar)
    
      tabs = gui.HGroup([1]*6)
      vg.getMember(1).add(tabs)

      mainbox = vg.getMember(2)

      keylabels = gui.HGroup([1]*4)
      vg.getMember(3).add(keylabels)

      t1=gui.TextBox()
      statusbar.getMember(0).add(t1)
      def cb1(temp):
        with t1.refreshHold:
          t1.text='%2.1f'%(temp*9.0/5.0+32)
        t1.refresh()
      ts = thermocouple.max6675((0,0))
#      ts = thermocouple.max6675(None)
      ts.report(cb1)


      t2=gui.TextBox()
      statusbar.getMember(5).add(t2)
      def cb2(tm):
        with t2.refreshHold:
          tm=tm.split('$')
          tm[1] = int(tm[1])
          t2.text='%s %u:%s %s'%tuple(tm)
        t2.refresh()
      clk = clock.Clock()
      clk.reportLocal(None, '%a$%I$%M$%p', cb2)

    
    while True:
      try:
        time.sleep(100)
      except KeyboardInterrupt:
        break

if __name__ == '__main__':
    main()


