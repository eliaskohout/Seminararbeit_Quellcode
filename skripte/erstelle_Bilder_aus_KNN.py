#!/bin/python3.8

import h5py
import cv2
import sys
from tensorflow.keras.models import load_model
import numpy as np

modell = load_model(sys.argv[1])
modell.save(f"./modell.h5")

hf = h5py.File('modell.h5', 'r')
encoder = hf.get('/model_weights/encoder')

for layer in encoder:
    if 'conv2d' not in layer: continue
    conv_layer = encoder.get(layer + '/kernel:0')

    print(conv_layer)
    for i in range(conv_layer.shape[3]):
        for j in range(conv_layer.shape[2]):
            kernelmap = conv_layer[0:5, 0:5, j, i]
            bild = cv2.normalize(kernelmap, np.zeros((5,5)), 0, 255, cv2.NORM_MINMAX)
            cv2.imwrite(f"daten/Bilder_Gewichte/CNN_{str(layer)}_({j},{i}).png", bild)
