# AWK-Skript, dass die train.log Datei eines Modells einliest und eine Liste der 'val_loss' Werte
# mit den Sekunden die bereits fürs Training verwendet wurden ausgibt. Wird von 'plot.sh' verwendet.
# 
# Output-Format:
# <Trainierte Sekunden>		<Loss-Wert zu dem Zeitpunkt>

func gibWert(pattern) {
	for(i=1; i<=NF; i++){
		if($i == pattern){return i+1;}
	}
	return 0;
}

BEGIN	{ FS = ";"; }

/Starte Training/{ letzter_zeitpunkt = $1 }
/val_loss/{ 
	dauer += $1-letzter_zeitpunkt;
	letzter_zeitpunkt = $1;
	print dauer, "\t", $gibWert("val_loss")
}
