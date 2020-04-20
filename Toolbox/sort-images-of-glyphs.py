#!/usr/bin/python3.4
# coding: utf8

import sys, os, subprocess, re
from lib.ProgressBar import *
import argparse
import yaml
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-r", "--rootfolder", help="root folder where sort is applying")
parser.add_argument("-o", "--output", help="folder to save the new sort")
parser.add_argument("-n", "--new", help="make a new sort in another folder [output]", action="store_true")
parser.add_argument("--hocrI", help="folder where are HOCRs files")
parser.add_argument("--hocrO", help="folder where saves modified HOCRs files")
args = parser.parse_args()

rootFolder = ""
outputFolder = ""
hocrFolder = ""
newHocrFolder = ""
new = False

# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile)
        rootFolder = configdata['extractedGlyphImageFolder']
        outputFolder = configdata['sortedGlyphImageFolder']
        hocrFolder = configdata['hocrFolder']
        # new = not bool(configdata['sortInSameFolder'])
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

if args.rootfolder is not None:
    rootFolder = args.rootfolder
if args.output is not None:
    outputFolder = args.output
if args.new is not None:
    new = bool(args.new)
if args.hocrI is not None:
    hocrFolder = args.hocrI
if args.hocrO is not None:
    newHocrFolder = args.hocrO
else:
    newHocrFolder = hocrFolder

if outputFolder[-1] != "/":
    outputFolder += "/"
subprocess.call(["mkdir", "-p", newHocrFolder])

if new is True and rootFolder == outputFolder:
    print("You can't create new folder with the same name ([root] = [output]) !")
    sys.exit()

if new is False:
    outputFolder = rootFolder
else:
    # subprocess.call(["cp", "-r", rootFolder, outputFolder])
    # subprocess.call(["find", rootFolder, "-type","f", "-name","'*'","-exec","cp","\{\}" ,outputFolder+"/.", "\\;"])
    print("copying "+rootFolder + " to " + outputFolder+"...")
    subprocess.call(["ToolboxV2/copy-folder.sh", rootFolder, outputFolder]) #tooo long !
    print("copy is done !")

listOutputFolder = os.listdir(outputFolder)  # list of the elements in the output folder

''' HOCR '''
hocrFiles = [hocrFolder + f for f in os.listdir(hocrFolder) if f.find('.hocr') != -1]
hocrFiles = sorted(hocrFiles)
HOCRs = {}
allGlyphs = []
print(hocrFiles)
for i,f in enumerate(hocrFiles):
    with open(f, "rb") as fp:
        pageHOCR = re.findall('\d+', f.split("/")[-1])[0]
        HOCRs[pageHOCR] = BeautifulSoup(fp, "lxml")
        allGlyphs += HOCRs[pageHOCR].find_all(attrs={"class": u"ocrx_cinfo"})


# Step one : sort unsorted images which are in the root folder
Bar1 = ProgressBar(len(listOutputFolder), 30, "Sort unsorted images (Step 1/2)")
for imgUnsorted in listOutputFolder:
    Bar1.update()
    if re.findall('.png', imgUnsorted):  # if this element is an image :
        # get the char name of the glyph
        glyphName = imgUnsorted[0]
        # create dir if it's necessary, move the image in this dir
        if glyphName == ".":  # to fix "." name
            subprocess.call(["mkdir", "-p", outputFolder + ".point"])
            subprocess.call(["mv", outputFolder + imgUnsorted, outputFolder + ".point/"])
        else:
            subprocess.call(["mkdir", "-p", outputFolder + glyphName])
            subprocess.call(["mv", outputFolder + imgUnsorted, outputFolder + glyphName])
            subprocess.call(["mkdir", "-p", outputFolder + glyphName + "/Italic"])
            subprocess.call(["mkdir", "-p", outputFolder + glyphName + "/Bold"])

# Step two : rename file if it does not correspond with the name of the folder in which it is.
# prepares the estimation of the process time.
totalFile = 0
nbfolder = 0
for r, d, f in os.walk(outputFolder):
    nbfolder += 1
    for i in f:
        totalFile += 1
totalFile -= nbfolder
Bar2 = ProgressBar(nbfolder, 30, "Resort " + str(totalFile) + " sorted images (Step 2/2)")


for folder in listOutputFolder:
    if not re.findall('.png', folder):  # found folders (not png files)
        if "autre" not in folder:  # Fix the ambiguous glyphs by hand by calling them "autre".
            for imgSorted in os.listdir(outputFolder + folder):
                Bar2.update()
                if re.findall('.png', imgSorted):
                    glyphName = imgSorted[0]
                    if glyphName == ".":  # fix "." name
                        if folder != ".point":
                            subprocess.call(
                                ["mv", outputFolder + folder + "/" + imgSorted, outputFolder + ".point/" + imgSorted])

                    elif glyphName != folder:
                        imgSortedBad = imgSorted
                        imgSortedGood = imgSortedBad.replace(glyphName, folder, 1)

                        subprocess.call(
                            ["mv", outputFolder + folder + "/" + imgSortedBad, outputFolder + folder + "/" + imgSortedGood])

                        globalGlyphCount = int(imgSortedBad.split(".")[-2].split("-")[-1])
                        fromPage = imgSortedBad.split(".")[-2].split("-")[2]
                        tmpNode = allGlyphs[globalGlyphCount]
                        tmpAttrs = tmpNode.attrs
                        oldText = tmpNode.string
                        try:
                            HOCRs[fromPage].find(attrs=tmpAttrs,text=oldText).string = folder
                        except AttributeError:
                            print("oups fail")
                        print(str(globalGlyphCount) +" : " +oldText +" --> "+folder)

                        # subprocess.call(["mv",rootFolder+folder+"/"+imgSorted,rootFolder+glyphName+"/"+imgSorted])

#print(HOCRs["336"].find(attrs={"class": u"ocrx_cinfo"}))

for nPage, hocr in HOCRs.items():
    html = hocr.encode("utf-8")
    with open(newHocrFolder+"p"+nPage+".hocr", "wb") as file:
        file.write(html)
