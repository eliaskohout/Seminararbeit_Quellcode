#!/bin/bash

python3.8 skripte/_speichere_modell_als_h5.py $1

mkdir -p ./daten/Bilder_Gewichte
h5dump modell.h5 |  awk -f skripte/_gib_gewichte_aus_h5dump.awk - | python skripte/_erstelle_Bilder_aus_Gewichten.py

rm modell.h5
