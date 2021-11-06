/{/ && gruppe_model_weights { gruppe_model_weights++ }
/}/ && gruppe_model_weights { gruppe_model_weights-- }

/{/ && gruppe_model_weights && gruppe_layers_1 { gruppe_layers_1++ }
/}/ && gruppe_model_weights && gruppe_layers_1 { gruppe_layers_1--; if(!gruppe_layers_1) sub(" >.*$", "", gruppen_namen); }

/{/ && gruppe_model_weights && gruppe_layers_2 { gruppe_layers_2++ }
/}/ && gruppe_model_weights && gruppe_layers_2 { gruppe_layers_2--; if(!gruppe_layers_2) sub(" >.*$", "", gruppen_namen); }

/GROUP "model_weights"/ { gruppe_model_weights = 1; gruppen_namen = "model_weights" }

/GROUP/ && !/model_weights/ && gruppe_model_weights {
	gsub("\"", "", $2);
	if(!gruppe_layers_1) { gruppe_layers_1 = 1; }
	else { gruppe_layers_2 = 1; }
	gruppen_namen = gruppen_namen " > " $2;
	print "\n#G " gruppen_namen;
}

/(.*): / && gruppe_model_weights && gruppe_layers_1 && gruppe_layers_2 {
	if( !match($1, idx_regex) || !idx_regex) {
		idx_regex = $1;
		sub("[0-9]+\\):", "[0-9]+\\):", idx_regex);
		sub("\\(", "\\(", idx_regex);
		name = idx_regex
		gsub("[\\\\|:]", "", name)
		print "\n#N " name;
	}
	printf("%.4f %.4f %.4f %.4f ", $2, $3, $4, $5);
}
