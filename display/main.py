from __future__ import division
##
 #  @filename   :   main.cpp
 #  @brief      :   4.2inch e-paper display (B) demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     August 15 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd4in2b
import Image
import ImageFont
import ImageDraw
import ImageMath

import sys
sys.path.append('..')
import thermocouple


def textbox(draw, text, size, fill=128, center=None, corner=None, align='center'):
    pt=96
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', pt)
    h,w = draw.multiline_textsize(text, font = font)
    if size[0]:
        s=size[0]/h
    if size[1]:
        s1=size[1]/w
        s=min(s,s1)
    pt=int(pt*s)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', pt)
    if center:
        h,w = draw.multiline_textsize(text, font = font)
        corner=center[0]-h/2, center[1]-w/2    
    draw.multiline_text(corner, text, font = font, fill = fill, align=align)
    

class Screen(object):
  def __init__(self, spi):
    epd = epd4in2b.EPD(spi)
    epd.init()
    self.epd=epd
    self.lastimage=None
    self.partials=0

  def _load(self, image, full=False):
    if self.partials > 5:
      full=True

    image = image.convert('1', dither=Image.FLOYDSTEINBERG)

    if self.lastimage and not full:
      diff = ImageMath.eval("a-b", a=self.lastimage, b=image)
      box = diff.getbbox()
      if box==None:
        return
      bits1 = self.epd.get_frame_window_buffer(self.lastimage, box)
      bits2 = self.epd.get_frame_window_buffer(image, box)
      self.epd.display_frame_window(bits1, bits2, box)
      self.partials+=1

    else:
      if self.lastimage:
        bits1 = self.epd.get_frame_buffer(self.lastimage)
      else:
        bits1 = None
      bits2 = self.epd.get_frame_buffer(image)

      self.epd.display_frame(bits1, bits2)
      self.partials=0
    self.lastimage=image


  def refresh(self, full=False):
      image = Image.new('L', (epd4in2b.EPD_WIDTH, epd4in2b.EPD_HEIGHT), 255)
      draw = ImageDraw.Draw(image)
      self.draw(draw)
      self._load(image, full)
      image.show()


  def draw(self, draw):

  #    draw_black.rectangle((0, 6, 400, 30), fill = 0)
      temp = '%2.1f'%(t.read(True)*9.0/5.0+32)
  #    temp='Hi\nAsron'
      print temp
      textbox(draw, temp, size=(200,100), center=(200,150), fill = 0)
  #    draw_black.arc((40, 80, 180, 220), 0, 360, fill = 0)
      # display the frames


  def dxraw(self, draw, num=[
#'88.2',
'89.2',
'87.3',
#'88.2',
'88.7']):
      temp = num[0]
      del num[0]
      print temp
      textbox(draw, temp, size=(200,100), center=(200,150), fill = 0)
    
  
t = thermocouple.max6675(0,0)

def main():
    s=Screen((1,0))

    while True:
      s.refresh()

if __name__ == '__main__':
    main()
