#!/usr/bin/python3.5
# coding: utf8

import sys
import subprocess


filename = sys.argv[1].split("/")[-1]
lsName = filename.split("-")
id = lsName[2]+"-"+lsName[3]
subprocess.call(["/opt/nightly/firefox", "localhost:8000/Layout/WebViewer/#"+id])

#subprocess.call("/opt/nightly/firefox","--new-tab","coucou")