# coding: utf8

import re
from bs4 import BeautifulSoup


def margining(coord, w=0, h=0, W=0, H=0):
    coord[0] -= w
    coord[1] -= h
    coord[2] += W
    coord[3] += H
    return coord

def getFontFamily(hocr_glyph, stylised_nodes, fontStyles):
    styles = []

    for i, (cssSelector,fontStyle) in enumerate(fontStyles):
        if hocr_glyph in stylised_nodes[cssSelector]:
            styles.append(fontStyle) #glyph
        elif hocr_glyph.parent in stylised_nodes[cssSelector]:
            styles.append(fontStyle) #word
        elif hocr_glyph.parent.parent in stylised_nodes[cssSelector]:
            styles.append(fontStyle) #line
        elif hocr_glyph.parent.parent.parent in stylised_nodes[cssSelector]:
            styles.append(fontStyle) #paragraph
        elif hocr_glyph.parent.parent.parent.parent in stylised_nodes[cssSelector]:
            styles.append(fontStyle) #area

    styles = list(dict.fromkeys(styles)) # remove doubles
    styles.sort()
    if len(styles)>0:
        return "-".join(styles)
    else :
        return ""

def getTitleAttribute(hocr_element, attribute):
    title = hocr_element["title"]
    if attribute == 'bbox' or attribute == 'x_bboxes':
        result = re.findall(r"(bbox|x_bboxes)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", title)[0]
        return [int(r) for r in result[1:]]

    elif attribute == 'image':
        return re.findall(r"image\s+(?:\'|\")([^\"|\']+)(?:\'|\")", title)[0]  # be careful with the image path syntax in hocr file!

    elif attribute is None:
        return title

    elif attribute == 'baseline':
        try:
            results = re.findall(r'{}\s+([+-]?([0-9]*[.])?[0-9]+)\s([+-]?\d+)'.format(attribute), title)
            return (float(results[0][0]), float(results[0][2]))
        except IndexError:
            return(0,0)
    elif attribute == "x_conf" or attribute == "x_confs" or attribute == "x_wconf":
        try:
            result = re.findall(r'{}\s+(\d+)'.format(attribute), title)[0]
            return result
        except IndexError:
            return 0
    else:
        results = re.findall(r'{}\s+([+-]?([0-9]*[.])?[0-9]+)'.format(attribute), title)
        return float(results[0][0])

def zoning(imgPage, node, margin):
    # get glyph's coords (and parse from xml)
    coordCrop = getTitleAttribute(node, "bbox")

    # margining
    coordCrop = margining(coordCrop, margin, margin, margin, margin)

    # crop the image of in the glyph in the image of the page
    area = imgPage.crop(coordCrop)
    # outputName = char+pageNum+"-"+idNode+".png";
    # area.save(folderOutputPath+char+pageNum+"-"idGlyph+".png")
    return area
