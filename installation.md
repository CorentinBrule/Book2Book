# Installation

## Tesseract
- tesseract 4.1
- tessdata for your languages

## Inkscape

## Fontforge
`# apt install fontforge python-fontforge`

## Python Toolbox virtual environment(s)

Installer toutes les libraires python necessaires à l'utilisation des scripts. Dans un environnement virtuel :

```bash
$ python3 -m venv Toolbox/venv3
$ source Toolbox/venv3/bin/activate
(venv3)$ pip install -r Toolbox/requirements-py3.txt
```

Ormi les scripts interagissant avec Fontforge puisque la librairie de son API n'est disponible qu'en Python2.7 et sur les dépots GNU/Linux (je n'ai pas encore cherché à le faire fonctionné sur Windows/Mac)

Vous devrez jongler avec un autre virtual env :

```bash
$ python2 -m venv Toolbox/venv2
$ source Toolbox/venv2/bin/activate
(venv2)$ pip install -r Toolbox/requirements-py2.txt
```

Lancer un script avec la bonne version et le bon environnement python sans passer par l'activation de l'environnement dans la console :

```bash
$ Toolbox/venv3/bin/python3 Toolbox/mon_script.py #python3
$ Toolbox/venv2/bin/python2 Toolbox/mon_script.py #python2  
```
