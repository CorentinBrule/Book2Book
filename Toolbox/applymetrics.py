#!/usr/bin/env python
# coding=utf-8

import fontforge
import re, sys
import argparse
import yaml
import json

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-f", "--font", help="font source file")
parser.add_argument("-m", "--metrics", help="json file with metrics")
parser.add_argument("--resize", help="resize value applied during processing")
args = parser.parse_args()

metricsFile = ""
fontFile = ""
resize = 0

try:
    with open(args.configfile, "r") as configfile:
        configdata = yaml.load(configfile)
        fontFile = configdata['fontSourceFile']
        metricsFile = configdata['metricsFile']
        #resize = configdata['resizeForLevel']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.metrics is not None:
    metricsFile = args.metrics
if args.font is not None:
    fontFile = args.font
#if args.resize is not None:
    #resize = args.resize

#resize = int(re.findall(r"\d+", resize)[0]) / 100
font = fontforge.open(fontFile)

with open(metricsFile, 'r') as mf:
    metrics = json.load(mf)

resize = metrics["mult_to_cadratin"]

def kerningFont(font):
    try :
        font.addLookup("table", "gpos_pair", (), (("liga", (("latn", ("dflt")),)),))
    except EnvironmentError:
        print("Lookup Table already exists")

    try:
        font.addLookupSubtable("table", "subtable")
    except EnvironmentError:
        print("Lookup Subtable already exists")

    print(font.getLookupInfo("table"))
    for glyph in list(font.glyphs()):
        # charnum = fontforge.unicodeFromName
        # print(glyph)
        # glyph.addPosSub("subtable","f",-3)
        # print("ok")
        try:
            for glyphPair, rawKern in metrics["kerning"][glyph.glyphname].items():
                kern = rawKern * resize
                print(kern)
                print(glyph)
                glyphPairName = fontforge.nameFromUnicode(ord(glyphPair))
                print(glyphPairName)
                glyph.addPosSub("subtable", glyphPairName, int(kern)) #in fontforge, kerning value must be an integer


        except KeyError:
            print("metrics {} are not found".format(glyph))


#font.gpos_lookups

# space width
spaceChar = font.createMappedChar(" ")
spaceChar.width = float(metrics[" "])*resize
# kerning
kerningFont(font)

font.save()

# ligatures
"""
igature_name = 'f_l'
ligature_tuple = ('f', 'l')
font.AddLookup('ligatures','gsub_ligature', (),[['rlig',[['arab',['dflt']]]]])
font.AddLookupSubtable('ligatures', 'ligatureshi')
glyph = font.createChar(-1, ligature_name)
glyph.addPosSub('ligatureshi', ligature_tuple)
"""
