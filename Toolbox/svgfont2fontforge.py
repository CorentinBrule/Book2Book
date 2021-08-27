#!/usr/bin/env python3
# coding=utf-8

import fontforge
import xml.dom.minidom as minidom
import re, sys
import argparse
import yaml, json
import codepoints
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-s", "--svg", help="SVGFont source file")
parser.add_argument("-f", "--font", help="font source file")
parser.add_argument("-g", "--individualGlyphFolder",help="folder to save individual glyphs used in font")
args = parser.parse_args()

svgFile = ""
fontFile = ""
individualGlyphFolder = ""
metricsFile = ""

marginValue = 0
try:
    with open(args.configfile, "r") as configfile:
        configdata = yaml.load(configfile)
        svgFile = configdata['svgFontFile']
        fontFile = configdata['fontSourceFile']
        individualGlyphFolder = configdata['individualGlyphFolder']
        metricsFile = configdata['metricsFile']
        marginValue = configdata['hocrMarginPixel']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.svg is not None:
    svgFile = args.svg
if args.font is not None:
    fontFile = args.font
if args.individualGlyphFolder is not None:
    individualGlyphFolder = args.individualGlyphFolder

subprocess.call(["mkdir", "-p", individualGlyphFolder])

marginRescaledValue = 0
try:
    with open(metricsFile, "r") as mf:
        mectrics = json.load(mf)
        marginRescaledValue = float(marginValue) * float(mectrics['mult_to_cadratin'])
except IOError:
    print("Metrics file 'metrics.json' or 'mult_to_cadratin' value not found !")

outputFile = svgFile.split(".")[0] +".sfd"

font = fontforge.font()
# glypha = font.createMappedChar('a')

svgDom = minidom.parse(svgFile)
svgModel = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   height="1000"
   width="1000"
   version="1.1"
   >
</svg>
"""

svglyphs = svgDom.getElementsByTagName('glyphe')
svglyphlayers = [g for g in svgDom.getElementsByTagName('g') if
                 len(re.findall(r'GlyphLayer.*', g.getAttribute("inkscape:label"))) == 1]

print(svglyphlayers[0].getAttribute("inkscape:label"))

for layer in svglyphlayers:
    print("-------------------")
    layerName = layer.getAttribute("inkscape:label")
    glyphName = layerName.split("-")[-1]
    print(glyphName)
    if glyphName == "autre" or glyphName == "":
        continue
    print(layer.getAttribute("width")[0:-2])
    gwidth = float(layer.getAttribute("width")[0:-2])

    #try:
    ''' pour faire les combinés pour l'assemblage des diacritiques
    if strglyph == "à" or strglyph == "ù":
        uniCodePoint = fontforge.unicodeFromName("acutecomb") #accent aigu combiné
    elif strglyph == "é":
        uniCodePoint = fontforge.unicodeFromName("gravecomb") #accent grave combiné
    elif strglyph == "û" or strglyph == "î" or strglyph == "ô":
        uniCodePoint = fontforge.unicodeFromName("uni0302") # accent circonflex combiné
    elif strglyph == "ï" or strglyph == "ö" or strglyph == "ü" or strglyph == "ä":
        uniCodePoint = fontforge.unicodeFromName("uni0308")  # tréma combiné
    elif strglyph == "œ" or strglyph == "oe":
        uniCodePoint = fontforge.unicodeFromName("oe") # œ = ligature oe
    elif strglyph == "ç":
        uniCodePoint = fontforge.unicodeFromName("ccedilla") # ç et pas que la cédille
    elif strglyph == "fi" or strglyph == "ﬁ":
        uniCodePoint = fontforge.unicodeFromName("fi")  # ligature fi "uniFB01"
    else: # other glyphs
        print("non!")
        uniCodePoint = fontforge.unicodeFromName(strglyph)
    '''

    #if re.match(r"",strglyph):

    #uniCodePoint = codepoints.from_unicode(strglyph.decode('utf-8'))[0]
    uniCodePoint = fontforge.unicodeFromName(glyphName)
    #glyphName = fontforge.nameFromUnicode(uniCodePoint)
    print(uniCodePoint)
    print(glyphName)
    #fontglyph = font.createMappedChar(glyphName)
    fontglyph = font.createChar(uniCodePoint)
    tmpsvg = minidom.parseString(svgModel)
    #print(tmpsvg.toxml())
    tmpsvg.getElementsByTagName("svg")[0].appendChild(layer)
    pathtmpsvg = individualGlyphFolder + glyphName + ".svg"
    with open(pathtmpsvg, 'w') as f:
        print(type(tmpsvg))
        tmpsvg.writexml(f)

    fontglyph.importOutlines(pathtmpsvg)

    fontglyph.width = gwidth

    # correct the margin present since the extraction of the images.
    fontglyph.left_side_bearing = fontglyph.left_side_bearing-marginRescaledValue
    fontglyph.right_side_bearing = fontglyph.right_side_bearing-marginRescaledValue

    #except ValueError as e:
    #    print("glyph name error")

space = font.createMappedChar(" ")

# font.selection.all()
# font.autoWidth(200)

font.save(outputFile)
