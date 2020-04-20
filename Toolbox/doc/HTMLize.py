#!/usr/bin/python3.5
# coding=utf-8

import os,subprocess
from ProgressBar import *
import argparse
import yaml

# put all pages and images extracted of glyphs in a HTML file to show them easier.

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-o", "--output", help="output file")
args = parser.parse_args()

outputFile = ""
pagesImagesFolder = ""
extractedGlyphImageFolder = ""

# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile)
        pagesImagesFolder = configdata['pagesImagesFolder']
        extractedGlyphImageFolder = configdata['extractedGlyphImageFolder']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.output is not None:
    outputFile = args.output

allPages = [pagesImagesFolder+f for f in os.listdir(pagesImagesFolder) if f.find(".png")]
allGlyphs = []
for folder in os.listdir(extractedGlyphImageFolder):
    if os.path.isdir(extractedGlyphImageFolder+folder):
        allGlyphs += [extractedGlyphImageFolder+folder+"/"+f for f in os.listdir(extractedGlyphImageFolder+folder) if f.find(".png")]
print(allGlyphs)

with open(outputFile, "w") as fp:
    html = """
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
    <link />
    """

    html += """
    <div id="pages">
    """
    for f in allPages:
        id = f.split("/")[-1].split(".")[-2]
        html += """
        <img src='{0}' id='{1}' class="page" onerror="this.style.display='none'"/>
        """.format(f,id)
    html += """
    </div>
    """

    html += """
    <div id="glyphs">
    """
    for f in allGlyphs:
        html += """
        <div class="glyphdiv">
            <img src='{}' class="glyph" onerror="this.style.display='none'"/>
        </div>
        """.format(f)
    html += """
    </div>
    """

    html += """
        </body>
        </html>
        """
    fp.write(html)
