#!/usr/bin/python3
# coding: utf8

import os, subprocess, re
from lib.ProgressBar import *
import argparse
import yaml
import unicodedata
import fontforge, codepoints



parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-t", "--targetfolder", help="folder(s) containing images to be averaged.", nargs='+')
parser.add_argument("-o", "--output", help="folder to save the averaged image(s)")
parser.add_argument("-s", "--style", help="specify style(s) of the font familly", nargs="+")
args = parser.parse_args()

targetFolders = ""
outputFolder = ""
fontStyles = ["main"]
# add "basic" font style, like "labor"

try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        glyphsFolder = configdata['sortedGlyphImageFolder']
        outputFolder = configdata['averageFolder']
        for fontStyle in configdata['fontStyles']:
            fontStyles.append(fontStyle[1])

except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.targetfolder is not None:
    glyphsFolder = args.targetfolder
if args.output is not None:
    outputFolder = args.output
if args.style is not None:
    fontStyles = args.style

#outputFolder += "/" + styleFolder

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

def list_all_fullpath_images(d):
    try:
        return [os.path.join(d, f) for f in os.listdir(d) if re.search(r"\.png|\.PNG", f) and os.path.isfile(os.path.join(d, f))]
    except FileNotFoundError as e:
        print(e)
        return []


def str2glyphName(char):
    if char == ".point":
        char = "."
    codepoint = fontforge.unicodeFromName(char)
    if codepoint != -1:
        glyphName = fontforge.nameFromUnicode(codepoint)
    else :
        codes = codepoints.from_unicode(char)
        if len(codes) == 1:
            glyphName = fontforge.nameFromUnicode(codes[0])
        else :
            glyphName = char
    return glyphName


for fontStyle in fontStyles:
    styleFolder = glyphsFolder + "/" + fontStyle
    print(styleFolder)
    if os.path.isdir(styleFolder):
        if not os.path.exists(outputFolder + "/" + fontStyle):
            os.mkdir(outputFolder + "/" + fontStyle)

        glyphsFolders = [styleFolder + "/" + f for f in os.listdir(styleFolder) if os.path.isdir(styleFolder +"/"+ f)]
        bar = ProgressBar(len(glyphsFolders), 30, "Averaging :")
        for f in glyphsFolders:
            images = list_all_fullpath_images(f)

            glyphStr = f.split("/")[-1]
            glyphName = str2glyphName(glyphStr)


            subprocess.call(["convert"] + images + ["-average", outputFolder + "/" + fontStyle + "/" + str(glyphName) + ".png"])
            print(outputFolder + "/" + fontStyle + "/" + str(glyphName) + ".png")
            #bar.update()
    else:
        print("no folder found")
