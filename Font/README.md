# Import des contours
## Font SVG avec inkscape :
### en graphique :

- créer un document de type "canevas typographique" `Glyphes/font.svg`

- importer chaque glyphes (`Glyphes/vectors/*.svg`)

/!\ une matix se crée à l'import (de type matrix(1.3333333,0,0,1.3333333,277.26123,389.97951) ) et en copiant le tracé de la glyphe depuis inkscape vers le canvas typographique)

- définir un pourcentage d'échelle à appliquer sur toutes les glyphes pour s'adapter au cadratin (ou changer la taille du doc pour s'adapter aux tailles des glyphes ?)
ex : 345%

- appliquer les transformations aux tracés (et non au groupe qui l'entour) `extension/Modifier le chemin/Apply Transform`

- placer le tracé dans un calque typographique `extension/Typographie/Ajouter un calque de glyphe...`

- une fois chaque glyphe dans un calque typographique, l'extension va générer la font SVG automatiquement avec : `extension/Typographie/convertir les calques de glyphes en police SVG`

### script :

* `new_glyph_layer.py` : `org.inkscape.typography.newglyphlayer`, `<param name="unicode" type="string" ...`

* utiliser l'extension `layers2svgfont.py` pour la conversion.

* `importSVGinSVGFont.py` pour faire tout ça.
  ```
  python3.5 Toolbox/importSVGinSVGFont.py {vectorFiles} > {outputFile}
  python3.5 Toolbox/importSVGinSVGFont.py Glyphes/vectors2/*30pc10d.svg > Font/font.svg
  ```

## Font SVG to FontForge :
### Bonnes pratiques :
extrait de [DesignWithFontForge]( http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html) :

* garder la taille du cadratin à 1000 (donc 1000px dans la svgfont)

* configurer la baseline dans "Element > Font Info > General" :

  * desendante fontforge = *y* baseline inkscape

  * assendante fontforge = 1000 - *y*

* chaque attribut *d* des *path* doit terminer par un "*Z*" pour que les normales (intérieur/extérieur soit bonnes dans FontForge)


### structure d'une fonte SVG :
```
...
  <font
         horiz-adv-x="1024"
         id="font74"
         inkscape:label="fonte 1">
        <font-face
           units-per-em="1024"
           id="font-face76"
           font-family="SVGFont 1" />
        <missing-glyph
           d="M0,0h1000v1024h-1000z"
           id="missing-glyph78" />
        <glyph
           glyph-name="glyphe 1"
           id="glyph80"
           unicode="a"
           d="M ..."
           />
        ...
  </font>
...

```
X-path avec xml.etree :

* svg.findall('./{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide') #trouve les guides

* svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@{http://www.inkscape.org/namespaces/inkscape}label="baseline"]') #trouve le guide qui a comme nom baseline
### script
* l'extension `adjustSVG2Font` permet de placer et redimensionner les glyphes par rapport à la grille de la typo SVG

  * on récupère les glyphes et leur BBOX avec svgpathtools. -> (x0,y0,x1,y1) a = (253.8495, 649.43808, 271.0452283962141, 753.5576795047747) (pozXobj=Gauche,maxXobj=Droit,EM-maxZobj=haut,EM-pozYobj=bas)

* Le script `svgfont2fontforge` permet d'importer une fontsvg dans FontForge. Il exporte chaque calque en un fichier SVG puis importe chaque svg dans la glyphe correspondante du fichier FontForge.
#### python-fontforge :
la lib fontforge pour python : [ref ici ](dmtr.org/ff.php)

    * font = fontforge.open("Font/font.sfd")

    * newGlyph = font.createMappedChar("a")

    * système de "selection" comme sur l'interface pour faire une action sur plusieurs glyphes (comme autoWidth)

# Métriques :

* puisque le cadratin est égale à 1000, la chasse de base l'est aussi. Les approches correspondent aussi à la position du tracé dans le fichier SVG source.

* dans FontForge on peut faire des metrics automatiques (autoWidth) à partir de valeurs (separation, min, max). Est-ce qu'il ne faut pas plûtot utiliser les valeurs sorties en HOCR ?

* ce type de données sont formater dans des fichiers comme `AFM` (Adobe Font Metrics) regroupant rélages font et pour chaques paires de caractères.(Kerning)

* on peut importer ces paramètres dans fontforge avec `mergeFeatures` (et/ou LookUp ?) ou les rentrer avec `addPosSub`

* on peut faire les Kerning dans inkscape mais comment les importer dans FontForge ?
