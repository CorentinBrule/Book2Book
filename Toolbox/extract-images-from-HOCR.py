#!/usr/bin/python3.5
# coding: utf8

import os, subprocess, re
import argparse
import yaml
from ProgressBar import *

from PIL import Image
from bs4 import BeautifulSoup

import extracthocr

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-H", "--hocr", help="HOCR source files", nargs='+')
parser.add_argument("-i", "--image", help="images source files", nargs='+')
parser.add_argument("-m", "--margin", help="margin around raw HOCR charboxes")
parser.add_argument("-o", "--output", help="folder to save extracted images of glyphs")
args = parser.parse_args()

hocrSources = ""
imageSources = ""
outputFolder = ""
margin = 0


# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile)
        outputFolder = configdata['extractedGlyphImageFolder']
        hocrSources = [configdata['hocrFolder'] + f for f in os.listdir(configdata['hocrFolder']) if re.search(r"hocr|html",f)]
        imageSources = [configdata['pagesImagesFolder'] + f for f in os.listdir(configdata['pagesImagesFolder']) if re.search(r"png|jpg|tiff", f)]
        margin = configdata['hocrMarginPixel']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

# overwrite data from command line arguments
if args.output is not None:
    outputFolder = args.output
if args.image is not None:
    imageSources = args.image
if args.hocr is not None:
    hocrSources = args.hocr
if args.margin is not None:
    margin = args.margin

#check name and create outputFolder
if outputFolder[-1] != "/":
    outputFolder += "/"
subprocess.call(["mkdir", "-p", outputFolder])

print(len(hocrSources),len(imageSources))
#inputs sorted and matched
globalGlyphCount = 0
HOCRs = {}
imgs = {}
# check if the number of PAGE files and page image match.
if len(hocrSources) == len(imageSources):
    for f in hocrSources:
        # get page number and match it with it HOCR file parsed in a dictionary : HOCRs[<page>] = <page>.hocr
        pageHOCR = re.findall('\d+', f.split("/")[-1])[0]
        with open(f, "rb") as fp:
            HOCRs[pageHOCR] = BeautifulSoup(fp, "lxml")

    for i in imageSources:
        # get page number and match it with it .png file parsed by PIL in a dictionary : imgs[<page>] = <page>.png
        pageNum = re.findall('\d+', i)[0]
        imgs[pageNum] = Image.open(i)

    for pageNumber in sorted(HOCRs):  # page by page
        hocrDocument = HOCRs[pageNumber]
        imgPage = imgs[pageNumber]
        firstPage = hocrDocument.find(attrs={"class": u"ocr_page"})
        # xml browsing
        if firstPage is not None:
            nodeGlyphs = firstPage.find_all(attrs={"class": u"ocrx_cinfo"})

            if len(nodeGlyphs) > 0:

                BarByPage = ProgressBar(len(nodeGlyphs), 30, 'Extraction page ' + pageNumber)

                # unicodeChars = []
                coordsCorpList = []
                for n in nodeGlyphs:  # glyph by glyph

                    area = extracthocr.zoning(imgPage, n, margin)
                    confidenceValue = extracthocr.getTitleAttribute(n, "x_conf")
                    word = n.parent
                    try :
                        if word.get("class").find("ocrx_word") == -1:
                            word = word.parent
                    except AttributeError:
                        word = word.parent

                    try :
                        word_id = word.get('id')
                    except:
                        print(n)
                        print(word)

                    glyphName = n.get_text()

                    outputName = glyphName + "-" + str(int(confidenceValue)) + "-" + str(pageNumber) + "-" + str(word_id) + "-" + str(globalGlyphCount) + ".png"
                    if glyphName == ".":  # to fix "." name
                        subprocess.call(["mkdir", "-p", outputFolder + ".point"])
                        #subprocess.call(["mv", outputFolder + imgUnsorted, outputFolder + ".point/"])
                        area.save(outputFolder + ".point/" + outputName)
                    else:
                        subprocess.call(["mkdir", "-p", outputFolder + glyphName])
                        #subprocess.call(["mv", outputFolder + imgUnsorted, outputFolder + glyphName])
                        area.save(outputFolder + glyphName + "/" + outputName)
                        subprocess.call(["mkdir", "-p", outputFolder + glyphName +  "/Italic"])
                        subprocess.call(["mkdir", "-p", outputFolder + glyphName +  "/Bold"])

                    #area.save(outputFolder + outputName)
                    globalGlyphCount += 1
                    BarByPage.update()
                    #coordsCorpList.append(coordCrop)
        else:
            print("impossible to extract images from {}".format(pageNumber))

else:
    print("PAGE files and page image don't match")
