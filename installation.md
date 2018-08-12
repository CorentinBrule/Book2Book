# Installation

## Python Toolbox virtual environment(s)

```bash
$ python3 -m venv Toolbox/venv3
$ source Toolbox/venv3/bin/activate
(venv3)$ pip install -r Toolbox/requirements-py35.txt
```

installe toutes les libraires python necessaires à l'utilisation des scripts.

Ormi les scripts interagissant avec Fontforge puisque la librairie de son API n'est disponible qu'en Python2.7 et sur les dépots GNU/Linux (je n'ai pas encore cherché à le faire fonctionné sur Windows/Mac)

```bash
$ apt install python-fontforge
$ pip2.7 install codepoints
```
Si vous voulez jonglé avec un autre virtual env :
```
$ python2 -m venv Toolbox/venv2
$ source Toolbox/venv2/bin/activate
(venv2)$ pip install -r Toolbox/requirements-py27.txt
```
