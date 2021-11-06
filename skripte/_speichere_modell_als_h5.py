#!/bin/python3

from tensorflow.keras.models import load_model
import sys

modell = load_model(sys.argv[1])
modell.save(f"./modell.h5")
