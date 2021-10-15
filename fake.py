import tensorflow as tf
import Gesichterextrahierer as GE

NAME = "CNN_V2"
NAME_AUTOENCODER_A = "Biden"
NAME_AUTOENCODER_B = "Norris"

autoencoder_A = tf.keras.models.load_model(f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_A}/")
autoencoder_B = tf.keras.models.load_model(f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_B}/")

PFAD_KASKADE = './daten/cascades/haarcascade_frontalface_default.xml'

def fake(num_bild_tuple):
    global autoencoder_B
    i, bild = num_bild_tuple
    bild = bild.astype('float32')
    bild /= 255.0
    erg = autoencoder_B.predict(bild.reshape(1, 128, 128, 3))[0]
    print("\rAnzahl der ersetzten Gesichter: %d" % i, end='')
    erg *= 255.0
    return erg

g = GE.Gesichterextrahierer(PFAD_KASKADE)
g.lade('./Biden.mp4')
g.fuerGesichterMache(fake, 128, 10000, True)
