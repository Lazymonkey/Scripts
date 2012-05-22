#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''

#                 {/ ． ．\}
#                 ( (oo)   )
#+--------------oOOo---︶︶︶︶---oOOo------------------+
#     FileName  :           wartermark.py
#     Describe  :           take wartermark to your image
#     Author    :           Lazy.monkey™
#     Email     :           lazymonkey.me@gmail.com
#     HomePage  :           lazymonkey.is-programmer.com
#     Version   :           0.0.1
#     LastChange:           2012-05-21 14:57:55
#+------------------------------------Oooo--------------+


'''
'''
notes: 0. 请设定输出为png图片格式，以得到最佳效果
       1. 请设定字体为你系统内的字体
Usages: 0. python watermark.py source_img -l 'yourlogo' target_img
        1. python watermark.py source_img -t 'text you want' target_img
'''
from PIL import Image, ImageDraw, ImageFont
from math import atan, degrees
import sys
import os

TEXT_FONT = "/home/lazymonkey/.fonts/Fabada-regular.ttf"     # 规定所使用的字体
ALPHA     = True

def usage():
    if len(sys.argv) != 5:
        sys.exit("Usage: %s <options> <intput-image <text or logo> <output-image>"
                % os.path.basename(sys.argv[0]))

def logo4mark(filename, logo, outfilename):
    img      = Image.open(filename)
    logo_img = Image.open(logo)   # 要保证你的logo是透明的哟。。。废话！

    img.paste(logo_img, (img.size[0] - logo_img.size[0],
              img.size[1] - logo_img.size[1]), logo_img)
    img.save(outfilename)

def text4mark(filename, text, outfilename):
    img       = Image.open(filename).convert("RGB")
    watermark = Image.new("RGBA", (img.size[0], img.size[1]))
    draw      = ImageDraw.ImageDraw(watermark, "RGBA")
    font_size = 0
    ##
    # @brief 得到最佳字体大小
    while True:
        font_size += 1
        nextfont = ImageFont.truetype(TEXT_FONT, font_size)
        nexttextwidth, nexttextheight = nextfont.getsize(text)
        if nexttextwidth+nexttextheight/3 > watermark.size[0]:
            break
        font = nextfont
        textwidth, textheight = nexttextwidth, nexttextheight

    draw.setfont(font)
    draw.text(((watermark.size[0]-textwidth)/2,
               (watermark.size[1]-textheight)/2), text)
    watermark = watermark.rotate(degrees(atan(float(img.size[1])/
                                              img.size[0])),
                                 Image.BICUBIC)
    if ALPHA is True:   # 水印透明
        mask = watermark.convert("L").point(lambda x: min(x, 55))
    watermark.putalpha(mask)
    img.paste(watermark, None, watermark)
    img.save(outfilename)

if __name__ == "__main__":
    usage()
    if sys.argv[1] == '-l':
        logo4mark(*sys.argv[2:])
    if sys.argv[1] == '-t':
        text4mark(*sys.argv[2:])
