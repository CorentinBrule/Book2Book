# Installation

## Tesseract
- tesseract 4.1
- tessdata pour les langues que vous voulez traiter

## Inkscape

- potrace

## Fontforge
`# apt install fontforge python3-fontforge`

## Python Toolbox virtual environment(s)

Installer toutes les libraires python necessaires à l'utilisation des scripts. Dans un environnement virtuel :

utiliser l'option `--system-site-packages` pour pouvoir accéder à python3-fontforge depuis l'environement virtuel

```bash
$ python3 -m venv --system-site-packages Toolbox/venv
$ source Toolbox/venv/bin/activate
(venv)$ pip install -r Toolbox/requirements.txt
```

Lancer un script avec la bonne version et le bon environnement python sans passer par l'activation de l'environnement dans la console :

```bash
$ Toolbox/venv/bin/python3 Toolbox/mon_script.py
```
