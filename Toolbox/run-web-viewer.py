#!/usr/bin/env python3
# coding : utf-8

import argparse
import yaml
import json
import subprocess, os, re

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-p", "--port", help="port where run http server")
parser.add_argument("--app", help="")
parser.add_argument("--hocr", help="hocr folder")
parser.add_argument("--pages", help="pages folder")
parser.add_argument("--npages", help="number of pages (start,end)", nargs="+")
args = parser.parse_args()

port = 0
webViewerFolder = ""
hocrFolder = ""
pagesImagesFolder = ""
npages = (0, 0)

# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile)
        webViewerFolder = configdata['webViewerFolder']
        port = configdata['webViewerPort']
        hocrFolder = configdata['hocrFolder']
        pagesImagesFolder = configdata['pagesImagesFolder']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.port is not None:
    port = args.port
if args.app is not None:
    webViewerFolder = args.app
if args.hocr is not None:
    hocrFolder = args.hocr
if args.pages is not None:
    pagesImagesFolder = args.pages
if args.npages is not None:
    npages = args.npages

hocrPages = [f for f in sorted(os.listdir(hocrFolder)) if f.split(".")[-1] == "hocr"]

if npages == (0, 0):
    npages = (
        re.search(r"\d+", hocrPages[0].split(".")[0]).group(0), re.search(r"\d+", hocrPages[-1].split(".")[0]).group(0))

objconfig = {"debPage": npages[0], "finPage": npages[1], "hocrFolder": hocrFolder, "pageImageFolder": pagesImagesFolder}

with open(webViewerFolder + "config.json", "w") as configFile:
    configFile.write("config=" + json.dumps(objconfig))

print("config.json file edited from the YAML config file of the project")

subprocess.call(["python3", "-m", "http.server", str(port)])
