#!/bin/bash

# Bash-Skript, das aus den als Argumente übergebenen 'train.log' Dateien ein Diagramm macht.
# Verwendet AWK um die Daten zu formatieren und gnuplot um das Diagramm zu erstellen.

plot_befehl="plot "
for dateiname in $@; do
	name=$(echo $dateiname | awk 'BEGIN {FS="/";} { print $3 }' - | sed -e "s/DenseLayers\?_.*_//g" )  # Namen aus dem Pfad extrahieren
	dateiname_daten=plot-script_$name.temp
	awk -f skripte/gib_val_loss.awk $dateiname > $dateiname_daten  # Datei mit den zu plotenden Daten erstellen
	plot_befehl+="'$dateiname_daten' using (\$1/3600):2 title \"$(echo $name | sed -e "s/e-/x10\^-^/" )\" with line linewidth 4,"  # An den Plot-Befehl anfügen
done
echo $plot_befehl


GNUPLOT_COMMAND=$(cat << EOF
set xrange [-0.1:4];
set yrange [:];
set xlabel "Trainingzeit in Stunden" font ",16";
set xlabel offset 2;
set xtics offset 1;
set ylabel "Fehler" font ",16";
set ylabel offset -2;
set ytics offset -1;
set logscale y;
set grid;
set border 3;
set border linewidth 2;
set tics scale 1;
set tics font ",14";
set key font ",14";
set tics nomirror;
set terminal qt size 700, 400;
$plot_befehl
EOF
)

gnuplot -p -e "$GNUPLOT_COMMAND"  # Diagramm erstellen

rm -f plot-script_*.temp  # Zuvor erstellte Dateien entfernen
