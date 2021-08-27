#!/usr/bin/python3
# coding: utf8

import os, sys, subprocess, re
from lib.ProgressBar import *
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-t", "--target", help="image(s) to be vectorized.", nargs='+')
parser.add_argument("-o", "--output", help="folder to save the vector(s)")
parser.add_argument("--pnm", help="folder to save pnm tmp files")
parser.add_argument("--simple", help="number of simplification steps")
parser.add_argument("--html", help="if html output", action="store_true")
parser.add_argument("-l", "--level", help="validate level value")
parser.add_argument("-s", "--style", help="specify style(s) of the font familly", nargs="+")
args = parser.parse_args()

images = ""
vectorsFolder = ""
pnmFolder = ""
nbSimple = 0
levelValue = 0
ifHTML = False
fontStyles = ["main"]

try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        vectorsFolder = configdata['vectorsFolder']
        pnmFolder = configdata['pnmFolder']
        nbSimple = configdata['nbSimple']
        levelValue = configdata['validLevelValue']
        ifHTML = bool(configdata['ifHTML'])
        for fontStyle in configdata['fontStyles']:
            fontStyles.append(fontStyle[1])
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.target is not None:
    images = args.target
if args.output is not None:
    vectorsFolder = args.output
if args.pnm is not None:
    pnmFolder = args.pnm
if args.simple is not None:
    nbSimple = args.simple
if args.level is not None:
    levelValue = args.level
if args.html is not None:
    ifHTML = args.html
if args.style is not None:
    fontStyles = args.style

if levelValue != 0:
    images = [i for i in images if i.find(str(levelValue))!=-1]

subprocess.call(["mkdir", "-p", pnmFolder])
subprocess.call(["mkdir", "-p", vectorsFolder])


for style in fontStyles:
    outputFolder = vectorsFolder + "/" + style +"/"
    subprocess.call(["mkdir", "-p", outputFolder])
    styleFolder = configdata['levelsFolder'] +"/"+ style +"/"
    images = [ styleFolder +"/"+ f for f in os.listdir(styleFolder)]
    Bar = ProgressBar(len(images), 30, "Vectorisation : ")
    print(images)
    for i in images:
        print(i)
        iName = i.split("/")[-1].split(".")[-2]
        subprocess.call(["convert", i, pnmFolder + iName + ".pnm"])
        subprocess.call(["potrace", pnmFolder + iName + ".pnm", "-s", "-o", outputFolder + iName + ".svg"])
        clearSvg = subprocess.check_output(["Toolbox/venv2/bin/python2.7", "Toolbox/extensionInkscape/applytransform.py", outputFolder + iName + ".svg"])
        # print(clearSvg.decode("utf-8"))
        with open(outputFolder + iName + ".svg", 'wb') as f:
            clearSvg = re.sub(r'"/>', 'Z"/>', clearSvg.decode("utf-8"))
            f.write(bytes(clearSvg, 'utf8'))

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>svg viewer</title>
            <script src="raphael.min.js"></script>
            <script src="displayHandles.js"></script>
        </head>
        <body>"""

        # try multiple simplification
        for s in range(nbSimple):  # nb de simplification
            subprocess.call(["cp", outputFolder +"/" + iName + "-simpl" + str(s) + ".svg",
                             outputFolder +"/"+ iName + "-simpl" + str(s + 1) + ".svg"])
            # print("cp","Glyphes/vectors/"+iName+"-simpl"+str(s)+".svg","Glyphes/vectors/"+iName+"-simpl"+str(s+1)+".svg")
            subprocess.call(
                ["inkscape", "--verb=EditSelectAll", "--verb=SelectionSimplify", "--verb=FileSave", "--verb=FileQuit",
                 outputFolder +"/"+ iName + "-simpl" + str(s + 1) + ".svg"])
            # print("inkscape","--verb=EditSelectAll","--verb=SelectionSimplify","--verb=FileSave","--verb=FileQuit","Glyphes/vectors/"+iName+"-simpl"+str(s+1)+".svg")
            # subprocess.call(["inkscape","--verb=EditSelectAll","--verb=SelectionSimplify","--export-plain-svg='Glyphes/vectors/"+iName+"-simpl"+str(s+1)+".svg'","Glyphes/vectors/"+iName+"-simpl"+str(s)+".svg"])
            html += "\n<object class='obj' data='{}' width='200px' height='200px' onload='draw(this)'></object>".format(
                iName + "-simpl" + str(s + 1) + ".svg")

        html += """
        </body>
        </html>
        """
        if ifHTML:
            with open(outputFolder+"/" + iName + ".html", 'wb') as f:
                f.write(html.encode('utf8'))

        Bar.update()
