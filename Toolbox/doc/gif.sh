#! /bin/bash
LC_COLLATE=C convert *.png -delay 50 -gravity center -fill White -extent 1000x1000 level.mpg
