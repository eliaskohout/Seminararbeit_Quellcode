"""
Die Klasse LoggingCallback, erbt von tensorflow.keras.callbacks.Callback

Wird als Instanz beim Trianieren mit der fit-Methode als callback übergeben. Die Methoden, welche mit "on_..."
beginnen werden zu dem entsprechenden Zeitpunkt wärend des Trainingsprozesses aufgerufen und dokumentieren den
Trainingsvortschritt in der Datei 'train.log' im Verzeichnis des Modells. Bei jedem Trainingsbeginn wird ein
Gesicht von jeder der beiden Personen durch das Modell geschickt und im Verzeichnis 'Bilder' Abgespeichert.
"""

import tensorflow.keras.callbacks
import time, os, cv2
import numpy as np

class LoggingCallback(tensorflow.keras.callbacks.Callback):
    def __init__(self, pfad_modell: str, bild_A: list, bild_B: list):
        self.pfad_modell = pfad_modell
        self.bild_A = bild_A.reshape(1, 128, 128, 3)
        self.bild_B = bild_B.reshape(1, 128, 128, 3)
        try: os.mkdir(os.path.join(self.pfad_modell, 'Bilder/'))
        except FileExistsError: pass

    def log(self, text: str):
        with open(os.path.join(self.pfad_modell, 'train.log'), "a") as datei:
            datei.writelines("{};{}\n".format(time.time(), text) )

    def speichereBild(self, bild: list, pfad: str):
        bild = cv2.normalize(bild, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
        bild = bild.astype(np.uint8)
        cv2.imwrite(pfad, bild)

    def on_train_begin(self, logs=None):
        self.log("Starte Training;")
        predicted_A = self.model.predict(self.bild_A)[0]
        predicted_B = self.model.predict(self.bild_B)[0]
        self.speichereBild(predicted_A, os.path.join(self.pfad_modell, "Bilder/{}_Bild_A.png".format(time.time()) ))
        self.speichereBild(predicted_B, os.path.join(self.pfad_modell, "Bilder/{}_Bild_B.png".format(time.time()) ))

    def on_epoch_begin(self, epoch, logs=None):
        logString = "on_epoch_begin;epoch;{};".format(epoch)
        for key, val in logs.items():
            logString += "{};{};".format(key, val)
        self.log(logString)

    def on_epoch_end(self, epoch, logs=None):
        logString = "on_epoch_end;epoch;{};".format(epoch)
        for key, val in logs.items():
            logString += "{};{};".format(key, val)
        self.log(logString)

    def on_train_batch_begin(self, batch, logs=None):
        logString = "on_train_batch_begin;batch;{};".format(batch)
        for key, val in logs.items():
            logString += "{};{};".format(key, val)
        self.log(logString)

    def on_train_batch_end(self, batch, logs=None):
        logString = "on_train_batch_end;batch;{};".format(batch)
        for key, val in logs.items():
            logString += "{};{};".format(key, val)
        self.log(logString)
