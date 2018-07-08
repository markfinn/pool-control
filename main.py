
import gui
import thermocouple
import time


def main():
    g=gui.GuiScreen((1,0))
    t=gui.TextBox()
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
