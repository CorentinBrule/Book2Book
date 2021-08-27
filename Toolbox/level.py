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
parser.add_argument("-d", "--delta", help="level delta value", nargs="+")
parser.add_argument("-b", "--blur", help="blur value(s)", nargs="+")
parser.add_argument("-r", "--resize", help="mult for rescale images. If not filled, this script will try to find the 'mult_to_cadratin' value in 'matrics.json' file")
parser.add_argument("-s", "--style", help="specify style(s) of the font familly", nargs="+")

parser.add_argument("--tmp", help="folder to save resized images")
args = parser.parse_args()

metricsFile = ""
metrics = {}
images = ""
levelFolder = ""
levels = ""
deltas = []
resize = 1
resizedFolder = ""
fontStyles = ["main"]
blurs = []

try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        metricsFile = configdata['metricsFile']
        averageFolder = configdata['averageFolder']
        levelFolder = configdata['levelsFolder']
        levels = configdata['levelValues']
        deltas = [d for d in configdata['deltaValues']]
        blurs = [b for b in configdata["blurValues"]]
        resizedFolder = configdata['resizedFolder']
        for fontStyle in configdata['fontStyles']:
            fontStyles.append(fontStyle[1])
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
    levelFolder = args.output
if args.level is not None:
    levels = args.level
if args.delta is not None:
    deltas = args.delta
if args.resize is not None:
    resize = args.resize
if args.tmp is not None:
    resizedFolder = args.temp
if args.style is not None:
    fontStyles = args.style

subprocess.call(["mkdir", "-p", levelFolder])
subprocess.call(["mkdir", "-p", resizedFolder])

percentResize = str(resize*100)+"%"

for fontStyle in fontStyles:
    styleFolder = averageFolder + "/" + fontStyle
    images = [styleFolder+"/"+f for f in os.listdir(styleFolder)]
    BarGlyph = ProgressBar(len(images), 30, "Glyphs : ")
    outputFolder = levelFolder + "/" + fontStyle
    subprocess.call(["mkdir", "-p", outputFolder])

    for glyph in images:
        glyphName = glyph.split("/")[-1].split(".")[-2]  # get the name of the glyph
        # print(glyphName)

        # save rescale and modify versions
        if resize != 1:
            subprocess.call(["convert", glyph, "-resize", percentResize, resizedFolder + glyphName + ".png"]) #save a rescale version
            for blur in blurs:
                for delta in deltas:
                    for level in levels:
                        m = int(level) - delta / 2
                        M = int(level) + delta / 2
                        parameter = str(m) + "%," + str(M) + "%"  # ex : 45%,55% with level=50% and delta=10%
                        outputName = glyphName + "-" + str(level) + "pc" + str(delta) + "d" + "-" + blur + ".png"
                        subprocess.call(
                            ["convert", resizedFolder+glyphName+".png", "-blur", blur ,"-level", parameter, outputFolder + "/" + outputName])

        else:
            for level in levels:
                m = int(level) - delta / 2
                M = int(level) + delta / 2
                parameter = str(m) + "%," + str(M) + "%"  # ex : 45%,55% with level=50% and delta=10%
                outputName = glyphName + str(level) + "pc" + str(delta) + "d.png"
                subprocess.call(["convert", glyph, "-level", parameter, outputFolder + "/" + outputName])

                #BarLvl.update()

        BarGlyph.update()
