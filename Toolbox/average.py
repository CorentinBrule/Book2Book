#!/usr/bin/python3
# coding: utf8

import os, subprocess, re
from lib.ProgressBar import *
import argparse
import yaml


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-t", "--targetfolder", help="folder(s) containing images to be averaged.", nargs='+')
parser.add_argument("-o", "--output", help="folder to save the averaged image(s)")
args = parser.parse_args()

targetFolders = ""
outputFolder = ""

try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        targetFolders = [configdata['sortedGlyphImageFolder'] + f for f in
                         os.listdir(configdata['sortedGlyphImageFolder']) if
                         os.path.isdir(configdata['sortedGlyphImageFolder'] + f)]
        outputFolder = configdata['averageFolder']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.targetfolder is not None:
    targetFolders = args.targetfolder
if args.output is not None:
    outputFolder = args.output

subprocess.call(["mkdir", "-p", outputFolder])


def list_all_fullpath_images(d):
    return [os.path.join(d, f) for f in os.listdir(d) if re.search(r"\.png|\.PNG", f)]


if len(targetFolders) > 0:
    bar = ProgressBar(len(targetFolders), 30, "Averaging :")
    for f in targetFolders:
        images = list_all_fullpath_images(f)
        outputName = f.split("/")[-1]
        subprocess.call(["convert"] + images + ["-average", outputFolder + "/" + outputName + ".png"])
        bar.update()
else:
    print("no folder found")
