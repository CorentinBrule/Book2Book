#!/usr/bin/python3
# coding: utf8

import os, subprocess, re
import argparse
import yaml
from lib.ProgressBar import *

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-t", "--target", help="images to analysis layout", nargs='+')
parser.add_argument("-o", "--output", help="folder to save HOCR files")
parser.add_argument("-l", "--lang", help="language used by Tesseract (see man)")
args = parser.parse_args()

images2analysis = ""
outputFolder = ""
lang = ""
resolution = 300

# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        outputFolder = configdata['hocrFolder']
        images2analysis = [configdata['pagesImagesFolder'] + f for f in os.listdir(configdata['pagesImagesFolder'])]
        resolution = configdata["pagesResolution"]
        print(resolution)
        lang = configdata["ocrLanguage"]
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

# overwrite data from command line arguments
if args.output is not None:
    outputFolder = args.output
if args.target is not None:
    images2analysis = args.target
if args.lang is not None:
    lang = args.lang

# beginning
print("start {} \nanalysis from :{} \nto output folder : {}\nin language : {}\n".format(__file__, images2analysis, outputFolder, lang))
subprocess.call(["mkdir", "-p", outputFolder])

if len(images2analysis) > 0:
    progressBar = ProgressBar(len(images2analysis), 30, "Analysis : ")
    for img in images2analysis:

        if os.path.isfile(img) and re.search(r"\.png|\.PNG|\.jpg|\.jpeg|\.JPG|\.JPEG|\.tif|\.TIF|\.jp2", img):
            outputName = img.split("/")[-1].split(".")[0:-1]
            subprocess.call(
                ["tesseract", str(img), str(outputFolder) + str(outputName[0]), "-l", lang, "--dpi", resolution ,"-c", "tessedit_create_hocr=1", "-c", "hocr_char_boxes=1"])
        else:
            print(" ----> invalid file found : {}".format(img))
        progressBar.update()
else:
    print("No files to analyze found :'(")
