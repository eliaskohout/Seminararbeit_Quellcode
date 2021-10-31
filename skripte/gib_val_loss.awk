func gibWert(pattern) {
	for(i=1; i<=NF; i++){
		if($i == pattern){return i+1;}
	}
	return 0;
}

BEGIN	{ FS = ";"; }

/Starte Training/{ letzter_zeitpunkt = $1 }
/val_loss/{ dauer += $1-letzter_zeitpunkt; letzter_zeitpunkt = $1; print dauer, "\t", $gibWert("val_loss")}
