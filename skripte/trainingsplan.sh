#!/bin/bash

run_with_latentspace_changed () {
	LATENT_SPACE=$1
	echo "Starte LatentSpace$LATENT_SPACE..." >> train.info
	sed -i "s/NAME = '.*'/NAME = 'DenseLayers_LatentSpace$LATENT_SPACE-SGD_lr=5e-1'/" Deepfake.py
	sed -i "s/tf\.keras\.optimizers\..*(.*)/tf.keras.optimizers.SGD(learning_rate=5e-1)/" Deepfake.py
	sed -i "s/Dense(.*)) #MARKER_LATENT_SPACE/Dense( $LATENT_SPACE )) #MARKER_LATENT_SPACE/" Deepfake.py
	sed -i "s/shape=(.*,) )) #MARKER_INPUT_DECODER/shape=($LATENT_SPACE,) )) #MARKER_INPUT_DECODER/" Deepfake.py
	sed -i "s/+.*#MARKER_ZEIT/+ 6*60*60 #MARKER_ZEIT/" Deepfake.py
	python Deepfake.py
}

run_with_latentspace_changed 100
