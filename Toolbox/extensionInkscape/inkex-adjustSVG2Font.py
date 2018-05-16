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

class adjustSVG2Font(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		# Get all the options

		#TODO: remove duplicate chars

		# Get access to main SVG document element
		svg = self.document.getroot()
		inkex.debug(svg)
		guides = svg.findall('./{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide')
		#print(guides)

		if len(guides)==0 :
			inkex.debug("No guide found.. Is SVG Font ?")
		else :
			baseline = svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="baseline"]').get("position")#trouve le guide qui a comme nom baseline et sort sa position
			ascender = svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="ascender"]').get("position")
			caps = svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="caps"]').get("position")
			xheight = svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="xheight"]').get("position")
			descender = svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="descender"]').get("position")
		#layers = svg.findall('.//g[@{http://www.inkscape.org/namespaces/inkscape}groupmode="layer"]')
		#layers = svg.xpath('//svg:g[@{http://www.inkscape.org/namespaces/inkscape}groupmode="layer"]', namespaces=inkex.NSS)
		layerGlyphs = [g for g in svg.xpath('//svg:g', namespaces=inkex.NSS) if g.get(inkex.addNS('groupmode', 'inkscape')) == 'layer' and len(re.findall(r'GlyphLayer.*',g.get(inkex.addNS('label', 'inkscape')))) == 1]

		for g in layerGlyphs:



if __name__ == '__main__':
	e = adjustSVG2Font()
	e.affect()
