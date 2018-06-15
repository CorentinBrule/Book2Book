# Numérisation des documents.

La première étape avant de reproduire un document est d'en posséder une version numérique. Pour celà, il existe deux possiblités :

* Numériser le document soi-même.
* Récupérer un fichier déjà existant.

Dans tout les cas, la qualité et la résolution de la numérisation aura un impact dans tout le processus de numérisation.

## Les fichiers déjà existant :

Il existe de nombreuses plateformes qui proposent des documents à télécharger. En effet, ...
Dans le cas des œuvres du domaine public, le leader de la numérisation est GoogleBooks...

Par exemple ce livre de 1839 n'est disponible (pour le moment) que sur GoogleBooks :

![](Book/industrie_francaise.png)

et (pas encore) sur *Internet Archive*

![](Book/internetarchive_not_found.png)

*"Peu importe ! Tant qu'il est disponible gratuitement..."*

Mais la license de GoogleBooks est, entre autre, imcompatible avec *Wikipedia*. Car Google interdit les usages comercials de ces scans d'œuvres élevé depuis longtemps dans le *domaine public*. Ce qui amène à des situations paradoxales comme celle-ci :

![](Book/wiki_Irony_punctuation.png)

L'article ne peut pas intégrer directement les passages intéressants. Une citation ne suffisant pas car l'article parle spécifiquement d'éléments graphiques de cet ouvrage. Le sourçage reste indirecte et l'information est plus complexe à transmettre sans illustrations.

![](Book/googlebooks_watermark.png)

Ce filigrame est la marque de propriété de l'entreprise américaine sur l'image du livre.

![](Book/googlebooks_contract.png)

<div style="page-break-after: always;"></div>

### `tpb.py` : bot de transfert GoogleBooks -> InternetArchive

Automatiser des action sur le web en simulant une activité *humaine* avec la librairie python `silenium`. Ce script utilise le driver de *Firefox* disponible sur le []()

## Les outils de numérisation :

La possession des outils de numérisation devient donc importante pour permettre le partage du patrimoine écrit. Si le scanner à plat s'est démocratisé avec l'imprimante de bureau, il ne convient pas aux formes écrites reliées. C'est pour cela que des comunautés travails sur des outils de numérisation DIY et open source pour rendre accéssible à ceux qui possède et qui veulent partager leur livres. [DIYBookScanner.org](http://diybookscanner.org/) regroupe par exemple des dizaines de designs différents de dispositif pour photographier les pages d'un livre dans les meilleurs conditions, selon les moyens et les compétences de chacuns.

![](Book/diy_book_scanner_schema.png)

### `bookscanner.py`

Ce script est basé sur la librairie `gphoto2` qui permet de contrôler les boiters d'appareil photo numérique.
<pre>
<code>gphoto2 --auto-detect</code> # lister les APN branché à l'ordinateur
<code>gphoto2 --capture-image</code> # prendre une photo
</pre>
Si on veut automatiser la prise de vue par ce dispositif, il faut choisir des APN compatibles avec la librairie (liste dispo avec `--list-cameras`) et jongler avec les modes de communication *PTP* ou *MTP*

`bookscanner.py` utilse le wrapper python de la librairie :
```
apt install libgphoto* && pip install gphoto2-cffi
```

Le reste du traitement des images se fait avec l'interface graphique de [ScanTailor](http://scantailor.org)
