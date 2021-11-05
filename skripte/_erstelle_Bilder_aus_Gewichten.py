"""

"""

import fileinput
import cv2
import numpy as np

for line in fileinput.input():
    line = line[:-1]
    if line == '': pass
    elif line[0:2] == '#G':
        gruppe = line[2:]
    elif line[0:2] == '#N':
        neuron = line[2:]
    else:
        gewichtungen = np.array([float(i) for i in line.split(' ') if i != ''])
        img_size = (int( np.sqrt( len(gewichtungen) ) ),)*2 + (1,)
        gewichtungen.resize(img_size)
        bild = cv2.normalize(gewichtungen, np.zeros((128,128)), 0, 255, cv2.NORM_MINMAX)
        cv2.imwrite(f"Layers/{gruppe}_{neuron}.png", bild)
