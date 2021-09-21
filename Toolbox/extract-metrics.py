#!/usr/bin/python3
# coding=utf-8

import os, sys, re, subprocess
from bs4 import BeautifulSoup
from PIL import Image
import extracthocr
from lib.ProgressBar import *
import argparse
import yaml
import json

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configfile", default="config.yaml")
parser.add_argument("-H", "--hocr", help="hocr(s) with layout data", nargs='+')
parser.add_argument("-i", "--image", help="image(s) of page", nargs='+')
parser.add_argument("--outputpair", help="folder to save the extracted images of pairs of letters ")
parser.add_argument("-m", "--metrics", help="json file to output metrics")
parser.add_argument("--capheight",help="define max letterheight to add multToCadratin to metrics")
args = parser.parse_args()

hocrSources = ""
imageSources = ""
outputPairFolder = ""
metricsFile = ""
margin = 0
capHeight = 0
cadratin = 0

# get data from config file
try:
    with open(args.configfile, "r", encoding="utf8") as configfile:
        configdata = yaml.load(configfile, Loader=yaml.FullLoader)
        # outputFolder = configdata['extractedGlyphImageFolder']
        hocrSources = [configdata['hocrFolder'] + f for f in os.listdir(configdata['hocrFolder']) if
                       re.search(r"hocr|html", f)]
        imageSources = [configdata['pagesImagesFolder'] + f for f in os.listdir(configdata['pagesImagesFolder']) if
                        re.search(r"png|jpg|tiff", f)]
        margin = configdata['hocrMarginPixel']
        metricsFile = configdata['metricsFile']
        capHeight = int(configdata['capHeight'])
        cadratin = configdata['cadratinSize']
except IOError:
    print("Config file 'config.yaml' not found or invalid !")

# overwrite data from command line arguments
# if args.output is not None:
    # outputFolder = args.output
if args.image is not None:
    imageSources = args.image
if args.hocr is not None:
    hocrSources = args.hocr
if args.metrics is not None:
    metricsFile = args.metrics
if args.capheight is not None:
    capHeight = int(args.capheight)
if args.outputpair is not None:
    outputPairFolder = args.outputpair


# alphabet = "abcdefghijklmnopqrstuvwxyzABCEDFGHIJKLMNOPQRSTUVWXYZ"  # aller plutot les chercher dans la font # ça ne sert à rien de rechercher Min+Maj (ex: eA), les majs doivent être traitées autrement
capAlphabet ="ABCDEFGHIJKLMNOP"

from itertools import chain, product


def bruteforce(charset, maxlength, minlength=1):
    return (''.join(candidate)
            for candidate in chain.from_iterable(product(charset, repeat=i)
                                                 for i in range(minlength, maxlength + 1)))


# all interlettrage by "bruteforce"
# all_ILs = list(bruteforce(alphabet, minlength=2, maxlength=2))


# print(all_ILs)

def extract_with_2_nodes(node0, node1, pageImg):
    coords0 = extracthocr.getTitleAttribute(node0, "bbox")
    coords1 = extracthocr.getTitleAttribute(node1, "bbox")
    print(coords0, coords1)
    print(coords1[0] - coords0[2])
    xs = sorted([coords0[0], coords0[2], coords1[0], coords1[2]])
    ys = sorted([coords0[1], coords0[3], coords1[1], coords1[3]])
    print(xs, ys)
    coordCrop = [xs[0], ys[0], xs[-1], ys[-1]]
    area = pageImg.crop(coordCrop)
    return area


def get_kern(node0, node1):
    coords0 = extracthocr.getTitleAttribute(node0, "bbox")
    coords1 = extracthocr.getTitleAttribute(node1, "bbox")
    kern = coords1[0] - coords0[2]
    return kern


# search without recursion
def search_string_in_tree(body, string):
    results_by_page = []
    # print(body.findAll(attrs={"class":"ocr_page"}))
    for page in body.findAll(attrs={"class": "ocr_page"}):
        if re.search(string, page.getText()):
            for area in page.findAll(attrs={"class": "ocr_carea"}):
                if re.search(string, area.getText()):
                    for para in area.findAll(attrs={"class": "ocr_par"}):
                        if re.search(string, para.getText()):
                            for line in para.findAll(attrs={"class": "ocr_line"}):
                                if re.search(string, line.getText()):
                                    for word in line.findAll(attrs={"class": "ocrx_word"}):
                                        if re.search(string, word.getText()):
                                            results_by_page.append(word)
    return results_by_page

# HERE ! #
def get_all_metrics(HOCRs):
    metrics = {" ": [], "baseline_angle": [], "baseline_offset": [], "x_size": [], "x_descenders": [],
               "x_ascenders": []}
    kerning = {}
    for page_number, hocrDoc in HOCRs.items():
        body = hocrDoc.body
        #print(page_number,hocrDoc)
        for page in body.findAll(attrs={"class": "ocr_page"}):
            if args.outputpair is not None:
                page_img = Image.open([i for i in imageSources if i.find(page_number) != -1][0])
            for area in page.findAll(attrs={"class": "ocr_carea"}):
                for para in area.findAll(attrs={"class": "ocr_par"}):
                    for line in para.findAll(attrs={"class": "ocr_line"}):
                        #print(line)

                        # extract metrics in hocrs's lines
                        metrics["x_size"].append(extracthocr.getTitleAttribute(line,"x_size"))
                        ba,bo = extracthocr.getTitleAttribute(line,"baseline")
                        metrics["baseline_angle"].append(ba)
                        metrics["baseline_offset"].append(bo)
                        metrics["x_descenders"].append(extracthocr.getTitleAttribute(line,"x_descenders"))
                        metrics["x_ascenders"].append(extracthocr.getTitleAttribute(line,"x_ascenders"))

                        words = line.findAll(attrs={"class": "ocrx_word"})
                        for i, word in enumerate(words):
                            if i > 0:
                                metrics[" "].append(get_kern(words[i-1], words[i])) # space
                                #print(get_kern(words[i-1], words[i]))
                            letters = word.findAll(attrs={"class": "ocrx_cinfo"})
                            for j, letter in enumerate(letters):
                                if j > 0:
                                    kern = get_kern(letters[j-1], letters[j])
                                    pair_name = letters[j - 1].get_text() + letters[j].get_text()
                                    kerning.setdefault(pair_name[0], {})
                                    kerning[pair_name[0]].setdefault(pair_name[1], []).append(kern) # kerns
                                    # print(kern)
                                    #print(letter)
                                    ## extract images of pairs:
                                    if args.outputpair is not None:
                                        area = extract_with_2_nodes(letters[j - 1], letters[j], page_img)
                                        word_id = word.get('id')
                                        output_name = pair_name + str(page_number) + "-" + word_id + "-" + str(
                                            j) + ".png"
                                        output_path = outputPairFolder + "/" + pair_name + "/"
                                        try:
                                            if not os.path.isdir(output_path):
                                                os.mkdir(output_path)
                                            area.save(output_path + output_name)
                                        except:
                                            print(
                                                "Can not create folder and/or save image. Maybe is a glyph name issue : " + output_path + output_name)

    metrics["kerning"] = kerning
    return metrics

def average_metrics(metrics):
    averaged = metrics.copy()
    for m in metrics:
        if m == "kerning":
            kerns = metrics[m]
            for glyph in kerns:
                for pair in kerns[glyph]:
                    # print(pair+" / "+glyph)
                    averaged["kerning"][glyph][pair] = float(sum(kerns[glyph][pair])) / len(kerns[glyph][pair])
        else :
            try:
                averaged[m] = float(sum(metrics[m])) / len(metrics[m])
            except ZeroDivisionError:
                averaged[m] = []
    return averaged

def get_multToCadratin(height,cadratin):
    return cadratin/height

# beginning !

HOCRs = {}
Imgs = {}

for f in hocrSources:
    # get page number and match it with it HOCR file parsed in a dictionnary : HOCRs[<page>] = <page>.hocr
    pageHOCR = re.findall('\d+', f.split('/')[-1])[0]
    with open(f, "rb") as fp:
        HOCRs[pageHOCR] = BeautifulSoup(fp,features="lxml")

for i in imageSources:
    # get page number and match it with it .png file parsed by PIL in a dictionnary : Imgs[<page>] = <page>.png
    pageImg = re.findall('\d+', i.split('/')[-1])[0]
    Imgs[pageImg] = Image.open(i)


metrics = get_all_metrics(HOCRs)
#print(metrics)

averaged = average_metrics(metrics)

if capHeight > 0:
    #print(capHeight)

    originalSize = capHeight + averaged["x_descenders"]
    #print(originalSize)
    averaged["mult_to_cadratin"] = get_multToCadratin(originalSize, cadratin)
else :
    averaged["mult_to_cadratin"] = configdata["multToCadratin"]

#print(averaged)

with open(metricsFile, 'w', encoding='utf8') as fp:
    # data = json.dumps(averaged)
    json.dump(averaged, fp)

'''
result_letters = {}
for il in all_ILs:
    results = {}
    print(il)
    for page_number, hocrDocument in HOCRs.items():  # page by page

        imgPage = Imgs[page_number]
        body = hocrDocument.body

        results_by_page = {}
        result_letters = {}

        result_words = search_string_in_tree(body, il)
        results_by_page[il] = result_words
        for rw in result_words:
            word = rw.findAll(attrs={"class": "ocrx_cinfo"})
            for i, letter in enumerate(word):
                if letter.get_text() == il[0] and word[i + 1].get_text() == il[1]:
                    # save on dictionnary

                    #if il in result_letters:
                    #    result_letters[il] += [(letter,word[i+1])]
                    #else :
                    #    result_letters[il] = [(letter,word[i+1])]


                    # extract kern
                    kern = get_kern(letter, word[i + 1])

                    result_letters.setdefault(letter, {})
                    result_letters[letter].setdefault(word[i + 1], []).append(kern)
                    # extract image
                    # area = extract_with_2_nodes(letter, word[i + 1], imgPage)
                    # outputName = il + str(page_number) + "-" + str(i) + ".png"
                    # area.save(folderOutputPath + outputName)
                    break

    # results_by_page = result_letters

print(result_letters)
'''

# test search with recursion
'''
def search_string_in_tree(element,string,end_tag,debug=False):
    if debug : print("- new search: "+string)
    def recursive_search_string_in_tree(element,string,end_tag,result,_debug):
        #if debug : print("---- new recursion :"+" in : \n"+ element.getText())

        if "class" in element.attrs:
            #if debug : print("class found -> "+str(element["class"]))
            if end_tag in element["class"]:
                #if debug : print("---------------word found -> "+element.getText())

                result.append(element)
                return
            else :
                pass
                #if debug : print("------------- no word found")

        else :
            pass
            #if debug : print("class no found")

        #if debug : print("-----found children ?"+ str(len(element.findChildren())))
        for child in element.findChildren():
            if debug : print(child.getText())
            if re.search(string,child.getText()):
                #if debug : print("---------word in child !")
                recursive_search_string_in_tree(child,string,end_tag,result,debug)
        #return

    result = []
    recursive_search_string_in_tree(element,string,end_tag,result,debug)
    return result
'''

# extract words
'''
results_by_page = {}
for il in all_ILs:
    result_words = search_string_in_tree(body,il,"ocrx_word",debug=True)
    results_by_page[il] = result_words
    for rw in result_words:
        firstChar = search_string_in_tree(rw,il[0],"ocrx_cinfo")
        print(firstChar)
        #secondChar = search_string_in_tree(rw,il[1],"ocrx_cinfo")
        #area = extracthocr.extract(pageImg,rw)
'''

'''
for il in results_by_page.keys():
    for i,r in enumerate(results_by_page[il]):
        area = extract_with_2_nodes(r[0],r[1])
        outputName = il + str(page_number) + "-" + str(i) + ".png"
        area.save(outputFolder + outputName)
'''
