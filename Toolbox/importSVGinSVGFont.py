#!/usr/bin/python3
# coding=utf-8

import sys, re, os
# import inkex
import xml.etree
import xml.etree.ElementTree
from lib.ProgressBar import *
import argparse
import subprocess
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-t", "--target", help="vector(s) to be imported in SVGFont.", nargs='+')
parser.add_argument("-o", "--output", help="folder to save the SVGFont")
parser.add_argument("-s", "--source", help="SVGFont source file")
args = parser.parse_args()

svgFontSource = ""
svgGlyphs = ""
outputFile = ""

try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        svgGlyphs = [configdata['vectorsFolder'] + f for f in os.listdir(configdata['vectorsFolder']) if f.split(".")[-1] == "svg"]
        outputFile = configdata['svgFontFile']
        svgFontSource = configdata['svgFontSourceFile']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.target is not None:
    svgGlyphs = args.target
if args.output is not None:
    outputFile = args.output
if args.source is not None:
    svgFontSource = args.source

doc = xml.etree.ElementTree.parse(svgFontSource)
xml.etree.ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
xml.etree.ElementTree.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
xml.etree.ElementTree.register_namespace("sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
xml.etree.ElementTree.register_namespace("cc", "http://creativecommons.org/ns#")

root = doc.getroot()
for glyph in svgGlyphs:
    glyphname = glyph.split("/")[-1][0]
    docglyph = xml.etree.ElementTree.parse(glyph)
    rootglyph = docglyph.getroot()
    gglyph = rootglyph.find('{http://www.w3.org/2000/svg}g')
    gwidth = rootglyph.get('width')
    gheight = rootglyph.get('height')
    gglyph.set("id", glyphname)
    # print(gglyph.tostring(encoding="utf-8"))
    # print(xml.etree.ElementTree.tostring(gglyph,encoding = "utf-8"))
    gglyph.set('inkscape:label', u'GlyphLayer-' + glyphname)
    gglyph.set('inkscape:groupmode', 'layer')
    gglyph.set('style', 'display:none')
    gglyph.set('width',gwidth)
    gglyph.set('height',gheight)
    root.append(gglyph)

    '''
    layer = xml.etree.ElementTree.SubElement(root, 'g')
    layer.set('inkscape:label', u'GlyphLayer-'+glyphname)
    layer.set('inkscape:groupmode', 'layer')
    layer.set('style', 'display:none')
    layer.append(gglyph)
    '''

doc.write(outputFile)

verticalAdjustedSvg = subprocess.check_output(["Toolbox/venv2/bin/python2.7", "Toolbox/extensionInkscape/inkex-adjustSVG2Font.py", outputFile])

with open(outputFile,'wb') as f:
    f.write(verticalAdjustedSvg)
# xml.etree.ElementTree.dump(docpython )
#print(xml.etree.ElementTree.tostring(root, encoding="utf-8").decode("utf8"))
