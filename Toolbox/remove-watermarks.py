#!/usr/bin/python3.5
# coding: utf8

import os, subprocess, re
import argparse
import yaml
from ProgressBar import *
from PIL import Image
#import numpy as np
#import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--images", help="images", nargs='+')
parser.add_argument("-b", "--bbox", help="bbox",help="x y w h",nargs='+')
args = parser.parse_args()

print(args.bbox)
x,y,w,h = args.bbox


'''white = np.zeros([int(w),int(h),3],dtype=np.uint8)
white.fill(125)
white_image = Image.fromarray(white)
'''
white_image = Image.new('RGB', (int(w),int(h)), (255, 255, 255))

#white_image.save("white.png")

Bar = ProgressBar(len(args.images), 30, "Pages : ")

for p in args.images:
    page = Image.open(p)
    page.paste(white_image,(int(x),int(y)))
    page.save(p)
    #subprocess.call(["convert",i,"\(white.png","-colorspace","gray","\)","-geometry", "+{}+{}".format(x,y),"-composite",i])
    Bar.update()