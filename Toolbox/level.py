#!/usr/bin/python3
# coding: utf8

import sys, os, subprocess, re
from lib.ProgressBar import *
import argparse
import yaml
import json

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-m", "--metrics", help="metrics json file")
parser.add_argument("-t", "--target", help="image(s) to be leveled.", nargs='+')
parser.add_argument("-o", "--output", help="folder to save the leveled image(s)")
parser.add_argument("-l", "--level", help="level value(s)", nargs='+')
parser.add_argument("-d", "--delta", help="level delta value")
parser.add_argument("-r", "--resize", help="mult for rescale images")
parser.add_argument("--tmp", help="folder to save resized images")
args = parser.parse_args()

metricsFile = ""
metrics = {}
images = ""
outputFolder = ""
levels = ""
delta = ""
resize = 1
resizedFolder = ""

try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        metricsFile = configdata['metricsFile']
        images = [configdata['averageFolder'] + i for i in os.listdir(configdata['averageFolder'])]
        outputFolder = configdata['levelsFolder']
        levels = configdata['levelValues']
        delta = configdata['deltaValue']
        resizedFolder = configdata['resizedFolder']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.metrics is not None:
    metricsFile = args.metrics

with open(metricsFile, 'r') as mf:
    metrics = json.load(mf)

if metrics is not None:
    try:
        resize = metrics["mult_to_cadratin"]
    except KeyError:
        print("mult_to_cadratin value is not find")

if args.target is not None:
    images = args.target
if args.output is not None:
    outputFolder = args.output
if args.level is not None:
    levels = args.level
if args.delta is not None:
    delta = args.delta
if args.resize is not None:
    resize = args.resize
if args.tmp is not None:
    resizedFolder = args.temp

subprocess.call(["mkdir", "-p", outputFolder])
subprocess.call(["mkdir", "-p", resizedFolder])

percentResize = str(resize*100)+"%"



BarGlyph = ProgressBar(len(images), 30, "Glyphs : ")

for glyph in images:
    glyphName = glyph.split("/")[-1][0]  # get the name of the glyph
    # print(glyphName)

    # save rescale and modify versions
    if resize != 1:
        subprocess.call(["convert", glyph, "-resize", percentResize, resizedFolder + glyphName + ".png"]) #save a rescale version
        for level in levels:
            m = int(level) - delta / 2
            M = int(level) + delta / 2
            parameter = str(m) + "%," + str(M) + "%"  # ex : 45%,55% with level=50% and delta=10%
            outputName = glyphName + str(level) + "pc" + str(delta) + "d.png"
            subprocess.call(
                ["convert", resizedFolder+glyphName+".png", "-level", parameter, outputFolder + "/" + outputName])

    else:
        for level in levels:
            m = int(level) - delta / 2
            M = int(level) + delta / 2
            parameter = str(m) + "%," + str(M) + "%"  # ex : 45%,55% with level=50% and delta=10%
            outputName = glyphName + str(level) + "pc" + str(delta) + "d.png"
            subprocess.call(["convert", glyph, "-level", parameter, outputFolder + "/" + outputName])

            #BarLvl.update()

    BarGlyph.update()
