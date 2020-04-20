#!/usr/bin/python3.5
# coding=utf-8

import os,subprocess
from ProgressBar import *
import argparse
import yaml

# put all images in a html file to show them easier.

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-t","--target",help="folder containing target images to be integrated in an html file.")
parser.add_argument("-o", "--output", help="output HTML file")
args = parser.parse_args()

outputFile = ""
target = ""

if args.output is not None:
    outputFile = args.output
if args.target is not None:
    target = args.target

allImages = [target+i for i in os.listdir(target) if i.find(".png")]
print(allImages)

with open(outputFile, "w") as fp:
    html = """
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="HTMLize-glyph.css">
    </head>
    <body>
    <link />
    """

    html += """
    <div id="images">
    """
    for f in allImages:
        html += """
        <div class="imagediv">
            <img src='{}' class="image" onerror="this.style.display='none'"/>
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
