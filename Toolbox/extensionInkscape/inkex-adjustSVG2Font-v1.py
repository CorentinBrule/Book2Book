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

import inkex
import sys
import locale
import re
import svgpathtools

class adjustSVG2Font(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def bbox_goup(self,group):
		paths = group.findall('svg:path', namespaces=inkex.NSS)
		bboxs = []
		# inkex.debug(paths)
		for path in paths:
			bboxs.append(svgpathtools.parse_path(path.get('d')).bbox())

		left = sorted([n[0] for n in bboxs])[0]
		right = sorted([n[1] for n in bboxs])[-1]
		top = sorted([n[2] for n in bboxs])[0]
		bot = sorted([n[3] for n in bboxs])[-1]
		'''
		bbox_group = (left,right,top,bot)
		inkex.debug(bboxs)
		inkex.debug(bbox_group)
		'''
		return (left,right,top,bot)


	def effect(self):
		# Get all the options
		baselineConstrainAlphabet = "abcdefhiklmnorstuvwxz"
		xheightConstrainAlphabet = "gjpqy"
		capContrainAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		#TODO: remove duplicate chars

		# Get access to main SVG document element
		svg = self.document.getroot()
		# inkex.debug(svg)
		guides = svg.findall('./{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide')
		#print(guides)
		withM = float(svg.get('width'))
		heightM = float(svg.get('height'))

		if len(guides) == 0 :
			inkex.debug("No guide found.. Is SVG Font ?")
		else :
			baseline = float(svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="baseline"]').get("position").split(',')[1]) # trouve le guide qui a comme nom baseline et sort sa position
			ascender = float(svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="ascender"]').get("position").split(',')[1])
			caps = float(svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="caps"]').get("position").split(',')[1])
			xheightPoz = float(svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="xheight"]').get("position").split(',')[1])
			descender = float(svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="descender"]').get("position").split(',')[1])
			xheight=xheightPoz-baseline

		#layers = svg.findall('.//g[@{http://www.inkscape.org/namespaces/inkscape}groupmode="layer"]')
		#layers = svg.xpath('//svg:g[@{http://www.inkscape.org/namespaces/inkscape}groupmode="layer"]', namespaces=inkex.NSS)
		layerGlyphs = [g for g in svg.xpath('//svg:g', namespaces=inkex.NSS) if g.get(inkex.addNS('groupmode', 'inkscape')) == 'layer' and len(re.findall(r'GlyphLayer.*',g.get(inkex.addNS('label', 'inkscape')))) == 1]
		xmult = 0
		for g in layerGlyphs :
			if g.get(inkex.addNS('label', 'inkscape')) == 'GlyphLayer-x':
				# xBBox =  svgpathtools.parse_path(g.find('svg:path', namespaces=inkex.NSS).get('d')).bbox() # remplacer par une fonction qui me retourne la bbox du groupe !
				xBBox = self.bbox_goup(g)
				rawxHeight = xBBox[3]-xBBox[2]
				xmult = xheight/rawxHeight

		for g in layerGlyphs:
			glyphName = g.get(inkex.addNS('label', 'inkscape'))[-1].encode('utf-8')
			inkex.debug(g.get(inkex.addNS('label', 'inkscape')).encode('utf-8'))
			inkex.debug(glyphName)
		 	if glyphName in baselineConstrainAlphabet or glyphName in xheightConstrainAlphabet or glyphName in capContrainAlphabet :
				path = g.find('svg:path', namespaces=inkex.NSS)
				if path is not None:
					pp = svgpathtools.parse_path(path.get('d'))
					# left,right,top,bot = pp.bbox()
					left,right,top,bot = self.bbox_goup(g)
					width = right-left
					height = bot-top
					#if inkex.debug(g.get(inkex.addNS('label', 'inkscape'))) == "GlyphLayer-a":
					#inkex.debug(top)
					#inkex.debug(height)
					if xmult == 0:
						mult = xheight/height # different mult for each glyph
					else:
						mult = xmult

					newHeight = height*mult
					moveY = heightM-top*mult-newHeight
					if glyphName in baselineConstrainAlphabet:
						moveY -= baseline
					elif glyphName in xheightConstrainAlphabet:
						moveY -= xheightPoz - newHeight
					elif glyphName in capContrainAlphabet:
						moveY -= baseline

					#path.set('transform','scale({0}) translate(0 {1})'.format(mult,moveY))
					g.set('transform','matrix({0},0,0,{0},0,{1})'.format(mult,moveY))
				else :
					inkex.debug("letter {} failed".format(glyphName))
if __name__ == '__main__':
	e = adjustSVG2Font()
	e.affect()
