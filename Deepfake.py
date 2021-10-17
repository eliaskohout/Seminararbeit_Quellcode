import numpy as np
import cv2
import os

def erstelleDatensatz(pfad: str, anzahl: int) -> list[list]:
    bilder = []
    for wurzel, ordner, dateien in os.walk(pfad):
        for datei in dateien:
            bild = cv2.imread(os.path.join(wurzel, datei))
            #bild = cv2.cvtColor(bild, cv2.COLOR_BGR2RGB)
            bild = bild.astype('float32')
            bild /= 255.0
            bilder.append(bild)
            if len(bilder) >= anzahl: break
            bilder.append(verzerren(bild, 10))
            if len(bilder) >= anzahl: break
            bilder.append(np.fliplr(bild))
            if len(bilder) >= anzahl: break
            bilder.append(verzerren(np.fliplr(bild), 10))
            if len(bilder) >= anzahl: break
    np.random.shuffle(bilder)
    bilder_train, bilder_test = teileListe(bilder, 0.75)
    bilder_train, bilder_test = np.array(bilder_train), np.array(bilder_test)
    print('%d Bilder aus %s geladen.' % (len(bilder), pfad))
    return [bilder_train, bilder_test]

def teileListe(liste: list, verteilung: float) -> list[list]:
    x = int(len(liste)*verteilung)
    return [liste[:x], liste[x:]]

def verzerren(bild: list, staerke: int):
    hoehe = bild.shape[0]
    breite = bild.shape[1]
    punkte_von = np.float32([[0, 0], [0, hoehe], [breite, 0], [breite, hoehe]])
    punkte_nach = np.float32([[0, staerke], [0, hoehe-staerke], [breite, 0], [breite, hoehe]])
    matrix = cv2.getPerspectiveTransform(punkte_von, punkte_nach)
    bild_verzerrt = cv2.warpPerspective(bild, matrix, (breite, hoehe))
    bild_verzerrt = bild_verzerrt[staerke:hoehe-staerke, staerke:breite-staerke]
    return cv2.resize(bild_verzerrt, (breite, hoehe))

datensatz_gesichter_A_train, datensatz_gesichter_A_test = erstelleDatensatz('./daten/lernen/Gesichter/A', 8192)
NAME_AUTOENCODER_A = 'Biden'

datensatz_gesichter_B_train, datensatz_gesichter_B_test = erstelleDatensatz('./daten/lernen/Gesichter/B', 8192)
NAME_AUTOENCODER_B = 'Putin'


# In[7]:


import tensorflow as tf

IMG_SHAPE = (128, 128, 3)
NAME = "CNN_V2"

def logSummary(string: str):
    with open(f"./daten/modelle/{NAME}/modell.info", "a") as datei:
        datei.write(string + "\n")

def gibEncoder():
    encoder = tf.keras.Sequential(name='encoder')
    encoder.add(tf.keras.layers.Conv2D(32, kernel_size=5, strides=2, padding='same', input_shape=( IMG_SHAPE ) ))
    encoder.add(tf.keras.layers.Conv2D(64, kernel_size=5, strides=2, padding='same'))
    encoder.add(tf.keras.layers.Conv2D(128, kernel_size=5, strides=2, padding='same'))
    encoder.add(tf.keras.layers.Conv2D(256, kernel_size=5, strides=2, padding='same'))
    encoder.add(tf.keras.layers.Flatten())
    encoder.add(tf.keras.layers.Dense( 500 ))

    encoder.summary(print_fn=logSummary)
    print(encoder.summary())
    return encoder

def gibDecoder():
    decoder = tf.keras.Sequential(name='decoder')
    decoder.add(tf.keras.layers.Dense( (8*8*256), input_shape=(500,)))
    decoder.add(tf.keras.layers.Reshape( (8, 8, 256) ))
    decoder.add(tf.keras.layers.Conv2DTranspose(256, kernel_size=5, strides=2, padding='same'))
    decoder.add(tf.keras.layers.Conv2DTranspose(128, kernel_size=5, strides=2, padding='same'))
    decoder.add(tf.keras.layers.Conv2DTranspose(64, kernel_size=5, strides=2, padding='same'))
    decoder.add(tf.keras.layers.Conv2DTranspose(32, kernel_size=5, strides=2, padding='same'))
    decoder.add(tf.keras.layers.Conv2DTranspose(3, kernel_size=1))

    decoder.summary(print_fn=logSummary)
    print(decoder.summary())
    return decoder


# In[2]:


def gibAutoencoder(name):
    x = tf.keras.layers.Input( shape=IMG_SHAPE, name='input_layer' )
    encoder, decoder = gibEncoder(), gibDecoder()
    autoencoder = tf.keras.Model(x, decoder(encoder(x)), name=name)

    print(autoencoder.summary())
    return autoencoder


# In[3]:


OPTIMIZER_FUNKTION = tf.keras.optimizers.Adam(learning_rate=1e-5)
LOSS_FUNKTION = tf.keras.losses.MeanSquaredError()

def gibKompiliertenAutoencoder(name):
    autoencoder = gibAutoencoder(name)
    autoencoder.compile(optimizer=OPTIMIZER_FUNKTION, loss=LOSS_FUNKTION)

    return autoencoder


# In[8]:


try:
    autoencoder_A = tf.keras.models.load_model(f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_A}/")
    autoencoder_B = tf.keras.models.load_model(f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_B}/")
    print("Modelle von der Festplatte geladen.")
except Exception as e:
    try:
        os.mkdir(f"./daten/modelle/{NAME}/")
        os.mkdir(f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_A}/")
        os.mkdir(f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_B}/")
    except FileExistsError:
        pass
    autoencoder_A = gibKompiliertenAutoencoder(name="autoencoder_A")
    autoencoder_B = gibKompiliertenAutoencoder(name="autoencoder_B")


# In[7]:


from tensorflow.keras.callbacks import ModelCheckpoint
import LoggingCallback as lc


autoencoder_A_logging_callback = lc.LoggingCallback(
    pfad_modell=f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_A}/",
    bild_A=datensatz_gesichter_A_test[1],
    bild_B=datensatz_gesichter_B_test[1]
)

autoencoder_B_logging_callback = lc.LoggingCallback(
    pfad_modell=f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_B}/",
    bild_A=datensatz_gesichter_A_test[1],
    bild_B=datensatz_gesichter_B_test[1]
)

autoencoder_A_checkpoint_callback = ModelCheckpoint(
    f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_A}/",
    monitor='val_loss',
    save_best_only=True
)

autoencoder_B_checkpoint_callback = ModelCheckpoint(
    f"./daten/modelle/{NAME}/{NAME_AUTOENCODER_B}/",
    monitor='val_loss',
    save_best_only=True
)


# In[9]:


import time, gc

ZEITPUNKT_ENDE = time.time() + int(100*60*60)

while time.time() < ZEITPUNKT_ENDE:
    print("!- Noch für ~{:.2f}h beschäftigt.".format(( ZEITPUNKT_ENDE-time.time() )/3600) )

    autoencoder_A.fit(
                      datensatz_gesichter_A_train,
                      datensatz_gesichter_A_train,
                      epochs=1,
                      batch_size=64,
                      shuffle=True,
                      validation_data=(datensatz_gesichter_A_test, datensatz_gesichter_A_test),
                      callbacks=[autoencoder_A_checkpoint_callback, autoencoder_A_logging_callback]
                     )
    autoencoder_B.layers[1] = autoencoder_A.get_layer('encoder')
    gc.collect()

    autoencoder_B.fit(
                      datensatz_gesichter_B_train,
                      datensatz_gesichter_B_train,
                      epochs=1,
                      batch_size=64,
                      shuffle=True,
                      validation_data=(datensatz_gesichter_B_test, datensatz_gesichter_B_test),
                      callbacks=[autoencoder_B_checkpoint_callback, autoencoder_B_logging_callback]
                     )
    autoencoder_A.layers[1] = autoencoder_B.get_layer('encoder')
    gc.collect()
