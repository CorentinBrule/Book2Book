#!/usr/bin/python
# coding: utf8

import subprocess, os
from shutil import copyfile

# p = principal script
# s = secondary script (not essential and link with manual operation)
# m = manual operation emulated
# d = create intermediate stages for visualisation and documentation 

copyfile("Toolbox/test/99.jpg","Pages/99.jpg")

# pillow show image page
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/olr-analysis.py","-c","Toolbox/test/config_test.yaml"])               # p
# tester la conformiter du document HOCR (avec python-hocr ?)
# subprocess.call(["python","Toolbox/test/test-hocr-edit.py"])                                             # m
# corriger le fichier HOCR avec une trancscription text fournie pour le test ?
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/extract-images-from-HOCR.py","-c","Toolbox/test/config_test.yaml"])   # p
#
# subprocess.call(["python","Toolbox/test/test-sort-glyphs.py"])                                           # m
#
# subprocess.call(["python","Toolbox/sort-images-of-char.py","-c","Toolbox/test/config_test.yaml"])        # s
#
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/extract-metrics.py","-c","Toolbox/test/config_test.yaml"])            # p
#
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/average.py","-c","Toolbox/test/config_test.yaml"])                    # p
#
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/level.py","-c","Toolbox/test/config_test.yaml"])                      # p
#
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/vectorize.py","-c","Toolbox/test/config_test.yaml"])                  # p
#
subprocess.call(["Toolbox/venv3/bin/python3","Toolbox/importSVGinSVGFont.py","-c","Toolbox/test/config_test.yaml"])         # p
#
# # change environement
subprocess.call(["python2","Toolbox/svgfont2fontforge.py","-c","Toolbox/test/config_test.yaml"])         # p
#
subprocess.call(["python2","Toolbox/applymetrics.py","-c","Toolbox/test/config_test.yaml"])              # p
