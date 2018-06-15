
# Métriques :

## extraction depuis l’HOCR

On peut essayer de générer les métriques de notre police de caractère de la même manière que nous avons fait pour les contours : en faisant la moyenne de tout les résultats individuels récupéré par *Tesseract* dans les fichiers *hOCR*. Plusieurs éléments peuvent nous intéresser :

* `x_size`
* `baseline_angle`
* `baseline_offset`
* `x_descenders`
* `x_assenders`

![](http://kba.cloud/hocr-spec/images/baseline.png)

* La taille de l’*espace* devrait être la distance entre les mots. (`ocrx_word`)
* Le *crenage* peut aussi être déduit de la position et de la taille des glyphs (`ocrx_cinfo`) deux à deux.

### script `extract-metrics.py`

Ce script va justement extraire toutes ces information des *hOCR*, en faire la moyenne et les enregistrer dans le fichier `Font/metrics.json`.

<pre>
<code>python3.5 extract-metrics.py [-c CONFIGFILE] [-H HOCR [HOCR ...]] [-i IMAGE [IMAGE ...]] [-m METRICS] [--capheight CAPHEIGHT]</code>
#exemple
<code>python3.5 extract-metrics.py -h Layout/hocr-charboxes -i Page/ --capheight 80</code>
</pre>

## Les metrics dans FontForge

* puisque le cadratin est égale à 1000, la chasse de base l’est aussi. Les approches correspondent aussi à la position du tracé dans le fichier SVG source.

* dans FontForge on peut faire des métriques automatiques (autoWidth) à partir de valeurs (separation, min, max). Est-ce qu’il ne faut pas plûtot utiliser les valeurs sorties en hOCR ?

* ce type de données sont formatées dans des fichiers comme `AFM` (Adobe Font Metrics) regroupant les réglages par groupe de caractère ou pour chaques paires de caractères.(*Crénage* ou *Kerning*)

* on peut importer ces paramètres dans fontforge avec `mergeFeatures` (et/ou LookUp ?) ou les rentrer avec `addPosSub`

* on peut faire le crenage dans inkscape mais comment les importer dans FontForge ?

# Import des contours
## Font SVG avec inkscape :

### structure d’une fonte SVG :

<div class="preblack">
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
</div>

*X-path* avec *xml.etree* :

`svg.findall('./{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview/{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide')` #trouve les guides

<code>svg.find('.//{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide[@</code> <code>{http://www.inkscape.org/namespaces/inkscape}</code> <code>label="baseline"]')</code> #trouve le guide qui a comme nom baseline

### en graphique :

* créer un document de type "*canevas typographique*" `Glyphes/font.svg`

* importer chaque glyphes (`Glyphes/vectors/*.svg`)

* /!\\ une matix se crée à l’import (de type matrix(1.3333333,0,0,1.3333333,277.26123,389.97951) ) et en copiant le tracé de la glyphe depuis inkscape vers le canevas typographique)*

* appliquer les transformations aux tracés (et non au groupe qui l’entoure) `extension` -> `Modifier le chemin` -> `Apply Transform`

* placer le tracé dans un calque typographique `extension` -> `Typographie` -> `Ajouter un calque de glyphe...`

* une fois chaque glyphe dans un calque typographique, l’extension va générer la font SVG automatiquement avec : `extension` -> `Typographie` -> `convertir les calques de glyphes en police SVG`

<div style="page-break-after: always;"></div>

### en script :

`importSVGinSVGFont.py` pour faire tout ça.
  <pre>
  <code>python3.5 Toolbox/importSVGinSVGFont.py {vectorFiles} > {outputFile}</code>
  <code>python3.5 Toolbox/importSVGinSVGFont.py Glyphes/vectors2/\*30pc10d.svg > Font/font.svg</code>
  </pre>

### script

l’extension `adjustSVG2Font` permet de placer et redimensionner les glyphes par rapport à la grille de la typo SVG

* on récupère les glyphes et leur BBOX avec svgpathtools. -> (x0,y0,x1,y1) a = (253.8495, 649.43808, 271.0452283962141, 753.5576795047747) *(pozXobj=Gauche,maxXobj=Droit,EM-maxZobj=haut,EM-pozYobj=bas)*

Chaque caractère va venir se placer à un endroit spécifique du canvas. Certain contours se poserons sur la *baseline*, d’autre en dessous de la *capheight* etc.

![](Font/svgfont.png)

<div style="page-break-after: always;"></div>

# Font SVG to FontForge :

### Bonnes pratiques :
extrait de [DesignWithFontForge]( http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html) :

* garder la taille du cadratin à 1000 (donc 1000px dans la svgfont)

* configurer la baseline dans "Element > Font Info > General" :

  * desendante fontforge = *y* baseline inkscape

  * assendante fontforge = 1000 - *y*

* chaque attribut *d* des *path* doit terminer par un "*Z*" pour que les normales (intérieur/extérieur soit bonnes dans FontForge)

## python-fontforge :

la lib fontforge pour python : [ref ici ](dmtr.org/ff.php)

*ne fonction qu’avec python 2.7*

petit guide rapide :

* `font = fontforge.open("Font/font.sfd")` # ouvre un fichier fontforge depuis python
* `newGlyph = font.createMappedChar("a")` # crée un caractère
* système de "selection" comme sur l’interface pour faire une action sur plusieurs glyphes (comme autoWidth) : `font.selection.all()` puis `font.autoWidth(200)`
* `font.save(newfont.sfd)`

### script
Le script `svgfont2fontforge` permet d’importer une *fontsvg* dans *FontForge*. Il exporte chaque calque en un fichier *SVG* puis les importe pour le caractère correspondant dans FontForge.
