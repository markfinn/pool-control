from __future__ import division

import display
import thermocouple

class Screen(display.Screen):
  def draw(self, draw):

  #    draw_black.rectangle((0, 6, 400, 30), fill = 0)
      temp = '%2.1f'%(t.read(True)*9.0/5.0+32)
  #    temp='Hi\nAsron'
      print temp
      display.textbox(draw, temp, size=(200,100), center=(200,150), fill = 0)
  #    draw_black.arc((40, 80, 180, 220), 0, 360, fill = 0)
      # display the frames

  
t = thermocouple.max6675(0,0)

def main():
    s=Screen((1,0))

    while True:
      s.refresh()

if __name__ == '__main__':
    main()
