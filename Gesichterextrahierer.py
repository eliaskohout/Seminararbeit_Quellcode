#!/usr/bin/python3

import sys, cv2, time, os
import numpy as np


class Gesichterextrahierer:
    def __init__(self, pfad_cascade: str):
        self.CASCADE = cv2.CascadeClassifier(pfad_cascade)

    def lade(self, pfad_video):
        self.PFAD_VIDEO = pfad_video
        self.video = cv2.VideoCapture(pfad_video)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))

    def play(self):
        while True:
            ist_bild, bild = self.video.read()
            if cv2.waitKey(1) == 27 or not ist_bild:
                break
            cv2.imshow('Deepfakeskript - Video', bild)
            time.sleep(1/self.fps-1)
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)
        cv2.destroyAllWindows()

    def fuerGesichterMache(self, funktion, bildgroesse_gesicht: int, max_anzahl_bilder: int, speichern=True) -> int:
        if speichern:
            pfad_Video_ohne_Endung = ".".join(self.PFAD_VIDEO.split(".")[:-1])
            video_writer = cv2.VideoWriter(f'{pfad_Video_ohne_Endung}_geändert.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_width, self.frame_height))
        ist_bild, bild = self.video.read()
        bild = np.array(bild)
        i = 0

        while ist_bild:
            bild_grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
            gesichter = self.CASCADE.detectMultiScale(bild_grau, 1.3, 5)
            for (x, y, breite, hoehe) in gesichter:
                if breite < bildgroesse_gesicht or hoehe < bildgroesse_gesicht:
                    continue
                gesicht = bild[y:y+hoehe, x:x+breite]
                gesicht_skaliert = cv2.resize(gesicht, (bildgroesse_gesicht, bildgroesse_gesicht))
                i += 1
                neues_Gesicht = funktion( (i, gesicht_skaliert) )
                if speichern:
                    neues_Gesicht_skaliert = cv2.resize(neues_Gesicht, (breite, hoehe))
                    bild[y:y+hoehe, x:x+breite] = neues_Gesicht_skaliert
                    video_writer.write(bild)
            ist_bild, bild = self.video.read()
            if i >= max_anzahl_bilder:
                break

        if speichern: video_writer.release()
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)
        return i

    def extrahiereGesichter(self, bildgroesse_ausgabe: int, max_anzahl_bilder: int, ordner_ausgabe: str):
        def funktion(num_bild_tuple):
            i, bild = num_bild_tuple
            cv2.imwrite(os.path.join(ordner_ausgabe, f'Gesicht_{i}.png'), bild)
            print("\r"+"Anzahl der extrahierten Bilder: %d" % i, end='')

        anzahl_extrahierter_bilder = self.fuerGesichterMache(funktion, bildgroesse_ausgabe, max_anzahl_bilder, speichern=False)
        print("\r"+"Es wurden erfolgreich %d Bilder nach %s exportiert." % (anzahl_extrahierter_bilder, ordner_ausgabe))


def main(argv):
    bildgroesse_ausgabe = 256
    max_anzahl_bilder = 50000
    pfad_cascade = "./daten/cascades/haarcascade_frontalface_default.xml"
    ordner_ausgabe = "./daten/Gesichter"

    for index, argument in enumerate(argv):
        if argument[0] == '-':
            if 'g' == argument[1]:
                bildgroesse_ausgabe = int(argv[index+1])
            elif 'a' == argument[1]:
                max_anzahl_bilder = int(argv[index+1])
            elif 'c' == argument[1]:
                pfad_cascade = argv[index+1]
            elif 'o' == argument[1]:
                ordner_ausgabe = argv[index+1]
            elif 'h' == argument[1]:
                print("Nutzung: %s [Optionen] [Videodatei]\n" % argv[0])
                print("""Optionen:
    -g : Größe der Ausgabe Bilder in Pixel
    -a : Maximale Anzahl der zu extrahierenden Bildern
    -c : Pfad für die Haarcascade
    -o : Zielordner für die Ausgabe
    -h : Drucken dieser Hilfenachricht""")

    g = Gesichterextrahierer(pfad_cascade)
    g.lade(argv[-1])
    g.extrahiereGesichter(bildgroesse_ausgabe, max_anzahl_bilder, ordner_ausgabe)


if __name__ == "__main__":
    main(sys.argv)
