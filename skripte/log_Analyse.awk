# Awk-Skript zum Analysieren der Log-Dateien, die beim Trainieren des Neuronalen Netzes anfallen
BEGIN	{ FS = ";"; }

func gibFeldnummer(pattern) {
	for(i=1; i<=NF; i++){
		if($i == pattern){return i;}
	}
	return 0;
}

func runden(zahl) {
	return int(zahl+0.5)
}

# Trainingsdauer -----------------------------------------------------------------------------------------
	{
	  if(match($0, "Starte Training")){
	    trainingsrunde_nr += 1
	    sekunden += vorheriger_Zeitstempel-zeitstempel_Start;
	    zeitstempel_Start = $1;
	    if(sekunden > 200000){print trainingsrunde_nr}
	  }
	  vorheriger_Zeitstempel = $1;
  	}
END	{
	  sekunden += vorheriger_Zeitstempel-zeitstempel_Start;
	  stunden = int(sekunden/3600); sekunden -= stunden*3600;
	  minuten = int(sekunden/60); sekunden -= minuten*60;
	  printf("Trainingsdauer:\t\t %sh %smin %ss\n", stunden, minuten, runden(sekunden));
  	}

# Anzahl/Dauer an Epochen -----------------------------------------------------------------------------------------
/on_epoch_begin/{ epochen++; epochen_start=$1;}
/on_epoch_end/{ avg_epochen_dauer += $1-epochen_start; avg_counter_epochen++;}
END	{avg_epochen_dauer /= avg_counter_epochen; printf("Epochen:\t\t %s a ~%ss\n", epochen, avg_epochen_dauer);}

# Anzahl/Dauer an Batches -----------------------------------------------------------------------------------------
/on_train_batch_begin/{ batches++; train_batch_start=$1;}
/on_train_batch_end/{ avg_train_batch_dauer += $1-train_batch_start; avg_counter_batch++;}
END	{avg_train_batch_dauer /= avg_counter_batch; printf("Trainierte Batches:\t %s a ~%ss\n", batches, avg_train_batch_dauer);}

# Loss -----------------------------------------------------------------------------------------
BEGIN	{ min_loss = 1000000000;}

/loss/ 	{
	  loss = $(gibFeldnummer("loss")+1);
	  avg_loss+=loss; x++;
	  if(max_loss < loss){max_loss=loss;};
  	  if(min_loss > loss){min_loss=loss;};
  	}
END	{
	  avg_loss /= x;
	  printf("LOSS (MIN/MAX/AVG):\t %.10f / %.10f / %.10f \n", min_loss, max_loss, avg_loss);
  	}

# Val Loss ------------------------------------------------------------------------------------
BEGIN	{ min_val_loss = 1000000000;}

/val_loss/{
	  val_loss = $(gibFeldnummer("val_loss")+1);
	  avg_val_loss+=val_loss; y++;
	  if(max_val_loss < val_loss){max_val_loss=val_loss;};
  	  if(min_val_loss > val_loss){min_val_loss=val_loss;};
  	}
END	{
	  avg_val_loss /= y;
	  printf("VAL_LOSS (MIN/MAX/AVG):\t %.10f / %.10f / %.10f \n", min_val_loss, max_val_loss, avg_val_loss);
  	}
