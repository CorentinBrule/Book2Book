#! /usr/bin/python
'''
Copyright (C) 2011 Felipe Correa da Silva Sanches

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import sys

sys.path.append('/usr/share/inkscape/extensions')
import inkex
import locale
import re
import svgpathtools


class adjustSVG2Font(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def bbox_goup(self, group):
        paths = group.findall('svg:path', namespaces=inkex.NSS)
        bboxs = []
        # inkex.utils.debug(paths)
        for path in paths:
            bboxs.append(svgpathtools.parse_path(path.get('d')).bbox())

        left = sorted([n[0] for n in bboxs])[0]
        right = sorted([n[1] for n in bboxs])[-1]
        top = sorted([n[2] for n in bboxs])[0]
        bot = sorted([n[3] for n in bboxs])[-1]

        # bbox_group = (left,right,top,bot)
        # inkex.utils.debug(bboxs)
        # inkex.utils.debug(bbox_group)
        return (left, right, top, bot)

    def effect(self):
        # Get all the options
        baselineConstrainGlyphs = "a,agrave,acircumflex,b,c,d,e,eacute,egrave,ecircumflex,edieresis,f,f_l,f_f,f_i,h,i,icircumflex,idieresis,k,l,m,n,o,ocircumflex,r,s,t,u,ucircumflex,v,w,x,z,oe,ae,Eacute,Ecircumflex,period,question,exclam,comma,colon,guillemotleft,guillemoright".split(",")
        xheightConstrainGlyphs = "g,j,p,q,y,ccedilla,three,four,five,seven,nine,semicolon".split(",")
        capContrainGlyphs = "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,zero,one,two,six,eight,parenleft,parenright,j,quotesingle,quoteright,numbersign".split(",")
        midXheightConstrainGlyphs = "hyphen,emdash".split(",")
        # TODO: remove duplicate chars
        # Get access to main SVG document element
        svg = self.document.getroot()
        # inkex.utils.debug(svg)
        guides = svg.findall(
            './{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide')
        # print(guides)
        withM = float(svg.get('width'))
        heightM = float(svg.get('height'))

        inkex.utils.debug(heightM)

        if len(guides) == 0:
            inkex.utils.debug("No guide found.. Is SVG Font ?")
        else:
            baselinePoz = float(svg.find(
                './/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="baseline"]').get(
                "position").split(',')[1])  # trouve le guide qui a comme nom baseline et sort sa position
            ascenderPoz = float(svg.find(
                './/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="ascender"]').get(
                "position").split(',')[1])
            capsPoz = float(svg.find(
                './/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="caps"]').get(
                "position").split(',')[1])
            xheightPoz = float(svg.find(
                './/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="xheight"]').get(
                "position").split(',')[1])
            descenderPoz = float(svg.find(
                './/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="descender"]').get(
                "position").split(',')[1])
            xheight = xheightPoz - baselinePoz
            inkex.utils.debug(xheight)
            capHeight = capsPoz - baselinePoz
            descenderDeep = descenderPoz - baselinePoz
            midXheight = xheight / 2
            midXheightPoz = baselinePoz + midXheight
            inkex.utils.debug(capHeight)
            inkex.utils.debug("=================")

        # layers = svg.findall('.//g[@{http://www.inkscape.org/namespaces/inkscape}groupmode="layer"]')
        # layers = svg.xpath('//svg:g[@{http://www.inkscape.org/namespaces/inkscape}groupmode="layer"]', namespaces=inkex.NSS)
        layerGlyphs = [g for g in svg.xpath('//svg:g', namespaces=inkex.NSS) if
                       g.get(inkex.addNS('groupmode', 'inkscape')) == 'layer' and len(
                           re.findall(r'GlyphLayer.*', g.get(inkex.addNS('label', 'inkscape')))) == 1]
        '''
        xmult = 0
        for g in layerGlyphs:
            if g.get(inkex.addNS('label', 'inkscape')) == 'GlyphLayer-x':
                # xBBox =  svgpathtools.parse_path(g.find('svg:path', namespaces=inkex.NSS).get('d')).bbox() # remplacer par une fonction qui me retourne la bbox du groupe !
                xBBox = self.bbox_goup(g)
                rawxHeight = xBBox[3] - xBBox[2]
                xmult = xheight / rawxHeight # multiplicateur pour que le "x" face la taille du xheight (pas implémenté)
        '''

        for g in layerGlyphs:
            glyphName = g.get(inkex.addNS('label', 'inkscape')).split("-")[1]
            inkex.utils.debug(glyphName)
            path = g.find('svg:path', namespaces=inkex.NSS)
            if path is not None:
                pp = svgpathtools.parse_path(path.get('d'))
                # left,right,top,bot = pp.bbox()
                left, right, top, bot = self.bbox_goup(g)
                width = right - left
                glyphHeight = bot - top
                # if inkex.utils.debug(g.get(inkex.addNS('label', 'inkscape'))) == "GlyphLayer-a":
                # inkex.utils.debug(top)
                # inkex.utils.debug(height)
                ''' je ne sais pas 
                if xmult == 0:
                    mult = xheight / height  # different mult for each glyph
                else:
                    mult = xmult
                '''

                mult = 1  # temp
                newHeight = glyphHeight * mult
                # moveY = heightM-top*mult-newHeight
                #moveY = heightM
                moveY=0
                inkex.utils.debug(glyphName in midXheightConstrainGlyphs)
                if glyphName in baselineConstrainGlyphs:
                    moveY = heightM - baselinePoz - glyphHeight - top
                elif glyphName in xheightConstrainGlyphs:
                    moveY = heightM - xheightPoz - top
                elif glyphName in capContrainGlyphs:
                    moveY = heightM - capsPoz - top
                    # inkex.utils.debug(moveY)
                    # inkex.utils.debug(baselinePoz)
                    # inkex.utils.debug(capHeight)
                    # inkex.utils.debug(capsPoz)
                    # inkex.utils.debug("--------")
                elif glyphName in midXheightConstrainGlyphs:
                    inkex.utils.debug(midXheightPoz)
                    inkex.utils.debug(midXheight)
                    moveY = heightM - midXheightPoz - top

                # path.set('transform','scale({0}) translate(0 {1})'.format(mult,moveY))
                g.set('transform', 'matrix({0},0,0,{0},0,{1})'.format(mult, moveY))
            else:
                inkex.utils.debug("letter {} failed".format(glyphName))


if __name__ == '__main__':
    e = adjustSVG2Font()
    e.run()
