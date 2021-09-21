#!/usr/bin/python3
# coding: utf8

import os, subprocess, re
import argparse
import yaml
from lib.ProgressBar import *

from PIL import Image
from bs4 import BeautifulSoup

import extracthocr

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-H", "--hocr", help="HOCR source files", nargs='+')
parser.add_argument("-i", "--image", help="images source files", nargs='+')
parser.add_argument("-m", "--margin", help="margin around raw HOCR charboxes", type=int)
parser.add_argument("-o", "--output", help="folder to save extracted images of glyphs")
parser.add_argument("-s", "--style", help="specific style(s)", nargs='+')
parser.add_argument("--mode", help="extraction mode : glyph by default")

args = parser.parse_args()

hocrSources = ""
imageSources = ""
outputFolder = ""
margin = 0
imageFolder = ""
fontStyles = ["main"]
cssSelectors = []
specificStyles = []
mode = "glyph"

# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        outputFolder = configdata['extractedGlyphImageFolder']
        hocrSources = [configdata['hocrFolder'] + f for f in os.listdir(configdata['hocrFolder']) if
                       re.search(r"hocr|html", f)]
        imageSources = [configdata['pagesImagesFolder'] + f for f in os.listdir(configdata['pagesImagesFolder']) if
                        re.search(r"png|jpg|tiff|tif|PNG|JPEG|JPG|jpeg|jp2", f)]
        imageFolder = configdata['pagesImagesFolder']
        margin = configdata['hocrMarginPixel']
        fontStyles = configdata['fontStyles']
        cssSelectors = configdata['cssSelectors']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

# overwrite data from command line arguments
if args.output is not None:
    outputFolder = args.output
if args.image is not None:
    imageSources = args.image
    imageFolder = args.image
if args.hocr is not None:
    hocrSources = args.hocr
if args.margin is not None:
    margin = args.margin
if args.style is not None:
    specificStyles = args.style
if args.mode is not None:
    mode = args.mode

# les styles s'ajoute des glyphs aux paragraphes
def getFontFamily(hocr_glyph, stylised_nodes, fontStyles):
    styles = []
    for style in fontStyles:

        family_nodes = stylised_nodes.get(style)
        if family_nodes is not None:
            if hocr_glyph in family_nodes:
                styles.append(style)  # glyph
            if hocr_glyph.parent in family_nodes:
                styles.append(style)  # word
            if hocr_glyph.parent.parent in family_nodes:
                styles.append(style)  # line
            if hocr_glyph.parent.parent.parent in family_nodes:
                styles.append(style)  # paragraph
            if hocr_glyph.parent.parent.parent.parent in family_nodes:
                styles.append(style)  # area

    styles = list(dict.fromkeys(styles))  # remove doubles
    styles.reverse()
    if len(styles) > 0:
        return "-".join(styles)
    else:
        return "main"


# check name and create outputFolder
if not os.path.isdir(outputFolder):
    os.mkdir(outputFolder)

for style in fontStyles:
    if not os.path.isdir(outputFolder + "/" + style):
        os.mkdir(outputFolder + "/" + style)

# print(len(hocrSources),len(imageSources))
# inputs sorted and matched
globalAreaCounter = 0
HOCRs = {}
imgs = {}

hocrSources.sort()

for f in hocrSources:
    # get page number and match it with it HOCR file parsed in a dictionary : HOCRs[<page>] = <page>.hocr
    pageHOCR = re.findall('\d+', f.split("/")[-1])[0]
    with open(f, "rb") as fp:
        HOCRs[pageHOCR] = BeautifulSoup(fp, "lxml")
    ocr_page_result = HOCRs[pageHOCR].select(".ocr_page")
    if len(ocr_page_result) == 1:
        ocr_page = ocr_page_result[0]
        page_image = extracthocr.getTitleAttribute(ocr_page, "image")
        print(page_image)
        page_image_path = page_image
        print(page_image_path)
        if os.path.isfile(page_image_path):
            print(page_image_path)
            imgs[pageHOCR] = Image.open(page_image_path)
            print(imgs[pageHOCR])
        else:
            imgs[pageHOCR] = Image.open(imageFolder + page_image_path)
print(imgs)

if len(imgs) == 0:
    print(":(")
    for i in imageSources:
        # get page number and match it with it .png file parsed by PIL in a dictionary : imgs[<page>] = <page>.png
        pageNum = re.findall('\d+', i)[0]
        print(pageNum)
        imgs[pageNum] = Image.open(i)

imageSources.sort()
# for f in hocrSources:
#     pageHOCR = re.findall('\d+', f.split("/")[-1])[0]
#     with open(f, "rb") as fp:
#         HOCRs[pageHOCR] = BeautifulSoup(fp, "lxml")
#     imgs[pageHOCR] = Image.open(imageSources[(int(pageHOCR) - 9)])

if len(HOCRs) == len(imgs):

    for pageNumber in sorted(HOCRs):  # page by page
        hocrDocument = HOCRs[pageNumber]
        imgPage = imgs[pageNumber]
        firstPage = hocrDocument.find(attrs={"class": u"ocr_page"})
        # xml browsing

        if firstPage is not None:
            nodeGlyphs = firstPage.find_all(attrs={"class": u"ocrx_cinfo"})

            if len(nodeGlyphs) > 0:

                BarByPage = ProgressBar(len(nodeGlyphs), 30, 'Extraction page ' + pageNumber)

                print(pageNumber)
                print(type(pageNumber))

                # unicodeChars = []
                coordsCorpList = []
                # find all element matched with cssSelector to find style of char
                stylised_nodes = {}
                for selector in cssSelectors:
                    stylised_nodes[cssSelectors[selector]] = []
                for selector in cssSelectors:
                    print(selector)
                    print(cssSelectors[selector])
                    stylised_nodes[cssSelectors[selector]] += hocrDocument.select(selector)

                if mode == "glyph":

                    for n in nodeGlyphs:  # glyph by glyph

                        confidenceValue = extracthocr.getTitleAttribute(n, "x_conf")
                        word = n.parent
                        try:
                            if word.get("class").find("ocrx_word") == -1:
                                word = word.parent
                        except AttributeError:
                            word = word.parent

                        try:
                            word_id = word.get('id')
                        except:
                            print(n)
                            print(word)

                        glyphStr = n.get_text()

                        # print(configdata["fontStyles"])
                        fontFamily = getFontFamily(n, stylised_nodes, fontStyles)
                        print(fontFamily)
                        if len(specificStyles) > 0 and not fontFamily in specificStyles:
                            continue
                        outputFolderFamily = outputFolder + "/" + fontFamily + "/"
                        if not os.path.isdir(outputFolderFamily):
                            os.mkdir(outputFolderFamily)

                        area = extracthocr.zoning(imgPage, n, margin)

                        outputName = glyphStr + "-" + str(int(confidenceValue)) + "-" + str(pageNumber) + "-" + str(word_id) + "-" + str(globalAreaCounter) + ".png"
                        if glyphStr == ".":  # to fix "." name
                            if not os.path.isdir(outputFolderFamily + ".point"):
                                os.mkdir(outputFolderFamily + ".point")
                            area.save(outputFolderFamily + ".point/" + outputName)
                        else:
                            if not os.path.isdir(outputFolderFamily + glyphStr):
                                os.mkdir(outputFolderFamily + glyphStr)
                            area.save(outputFolderFamily + "/" + glyphStr + "/" + outputName)

                        # area.save(outputFolder + outputName)
                        globalAreaCounter += 1
                        BarByPage.update()
                        # coordsCorpList.append(coordCrop)
                if mode == "word":
                    words = firstPage.find_all(attrs={"class": u"ocrx_word"})

                    for word in words:
                        fontFamily = getFontFamily(word, stylised_nodes, fontStyles)
                        if len(specificStyles) > 0 and not fontFamily in specificStyles:
                            continue

                        word_id = word.get('id')

                        wordStr = word.findAll(text=True, recursive=False)

                        if len(wordStr) > 0:
                            wordStr = wordStr[0]

                        outputFolderFamily = outputFolder + "/" + fontFamily + "/"
                        if not os.path.isdir(outputFolderFamily):
                            os.mkdir(outputFolderFamily)

                        outputName = wordStr + "-" + str(word_id) + "-" + str(globalAreaCounter)+ ".png"
                        globalAreaCounter += 1

                        area = extracthocr.zoning(imgPage, word, margin)
                        area.save(outputFolderFamily + "/" + outputName)

        else:
            print("impossible to extract images from {}".format(pageNumber))

else:
    print("HOCR files ({}) and page images ({}) don't match".format(len(HOCRs), len(imgs)))

if mode == "glyph":
    for style in fontStyles:
        stylePath = outputFolder + "/" + style + "/"
        for glyphFolder in os.listdir(stylePath):
            if os.path.isdir(stylePath + "/" + glyphFolder):
                for otherStyle in fontStyles:
                    if otherStyle != style:
                        otherStyleFolder = outputFolder + "/" + otherStyle + "/"
                        destinationLinkPath = os.path.abspath(stylePath + "/" + glyphFolder + "/" + otherStyleFolder)
                        sourcePath = "../../" + otherStyle + "/" + glyphFolder
                        print(sourcePath)
                        print(destinationLinkPath)
                        try:
                            os.symlink(sourcePath, destinationLinkPath, target_is_directory=True)
                        except FileNotFoundError:
                            pass
