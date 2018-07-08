from __future__ import division

import epd4in2b
import Image
import ImageFont
import ImageDraw
import ImageMath


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
    if spi==None:#dummy disply, not on rpi
      self.epd=None
    else:
      epd = epd4in2b.EPD(spi)
      epd.init()
      self.epd=epd
    self.lastimage=None
    self.partials=0

  def _load(self, image, full=False, wait=True):
    if self.partials > 5:
      full=True

    image = image.convert('1', dither=Image.FLOYDSTEINBERG)

    if self.epd==None:#dummy
      image.show()
      return

    if self.lastimage and not full:
      diff = ImageMath.eval("a-b", a=self.lastimage, b=image)
      box = diff.getbbox()
      if box==None:
        return
      bits1 = self.epd.get_frame_window_buffer(self.lastimage, box)
      bits2 = self.epd.get_frame_window_buffer(image, box)
      self.epd.display_frame_window(bits1, bits2, box, wait)
      self.partials+=1

    else:
      if self.lastimage:
        bits1 = self.epd.get_frame_buffer(self.lastimage)
      else:
        bits1 = None
      bits2 = self.epd.get_frame_buffer(image)

      self.epd.display_frame(bits1, bits2, wait)
      self.partials=0
    self.lastimage=image


  def refresh(self, full=False, wait=True):
      image = Image.new('L', (epd4in2b.EPD_WIDTH, epd4in2b.EPD_HEIGHT), 255)
      draw = ImageDraw.Draw(image)
      self.draw(draw)
      self._load(image, full, wait)
      image.show()


  def draw(self, draw):
      textbox(draw, "Hello, World!", size=(200,200), center=(200,150), fill = 0)


  @property
  def size(self):
    return epd4in2b.EPD_WIDTH, epd4in2b.EPD_HEIGHT


if __name__ == '__main__':
    s=Screen((1,0))
    s.refresh()
