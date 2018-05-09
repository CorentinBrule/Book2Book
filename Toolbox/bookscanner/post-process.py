#!/usr/bin/env python3
# coding : utf-8

import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="path")

args = parser.parse_args()

length = len(os.listdir(args.path))

files = [f for f in sorted(os.listdir(args.path)) if os.path.isfile(args.path+f)]
print(files)

## resize
size1 = eval(subprocess.check_output(["identify","-format",'[%w,%h]',args.path+files[0]]))
#print(type(eval(subprocess.check_output(["identify","-format",'"[%w,%h]"',args.path+sorted(os.listdir(args.path))[0]]))))
size2 = eval(subprocess.check_output(["identify","-format",'[%w,%h]',args.path+files[-1]]))
maxSize =[]
if size1[0] > size2[0]:
    maxSize = size1
else :
    maxSize = size2

print(maxSize)
for i, file in enumerate(sorted(os.listdir(args.path))):

    if (i < length / 2):
        n = i*2+1
        #name = args.path + str(n)+".jpg"
        name = args.path + file
        subprocess.call(["convert", args.path + file, "-rotate", "-90", "-resize", "{}x{}".format(maxSize[0],maxSize[1]) ,name])
    else:
        n = int(i-length/2)*2
        #name = args.path + str(n)+".jpg"
        name = args.path + file
        subprocess.call(["convert", args.path + file, "-rotate", "90", "-resize", "{}x{}".format(maxSize[0],maxSize[1]) ,name])

subprocess.call(["scantailor"])

output_path = args.path+"out/"
for page in os.listdir(output_path):
    if page.split(".")[-1] == "tif":
        subprocess.call(["mv",output_path+page,output_path+page[1:]])

subprocess.call(["convert",output_path+"*.tif","-density","400","book.pdf"])