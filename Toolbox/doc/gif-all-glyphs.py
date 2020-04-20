import imageio

import os, subprocess, re
import argparse
import yaml
from ProgressBar import *

# create gifs for each glyph with extracted images and put them in html file

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-G", "--glyphs", help="Glyphes folder")
parser.add_argument("-o", "--output", help="folder to save generated gif")
args = parser.parse_args()

glyphFolder = ""
outputFolder = ""


# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile)
        glyphFolder = configdata['extractedGlyphImageFolder']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

# overwrite data from command line arguments
if args.glyphs is not None:
    glyphFolder = args.glyphs
if args.output is not None:
    outputFolder = args.output
else:
    outputFolder = "."

subprocess.call(["mkdir","-p",outputFolder])

gifList = []

folders = sorted(os.listdir(glyphFolder))
Bar = ProgressBar(len(folders), 30, 'Create gif ')


for folder in folders:
    gifName = folder+'.gif'
    gifList.append(gifName)

    with imageio.get_writer(outputFolder+"/"+gifName, mode='I') as writer:
        if os.path.isdir(glyphFolder + folder):
            files = [glyphFolder + folder + "/" + f for f in sorted(os.listdir(glyphFolder+folder)) if f.split(".")[-1] == "png"]
            for filename in files:
                image = imageio.imread(filename)
                writer.append_data(image)


    Bar.update()


with open(outputFolder+"gif.html","w") as fp:
    html = """
    <html>
    <head><meta charset="UTF-8"></head>
    <body>
    """

    for g in gifList:
        html += """
        <img src='{}' onerror="this.style.display='none'"/>
        """.format(g)

    html +="""
        </body>
        </html>
        """
    fp.write(html)
