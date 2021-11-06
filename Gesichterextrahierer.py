#!python3.8
import sys, cv2, time, os
import numpy as np
import face_recognition


class Gesichterextrahierer:
    def __init__(self, pfad_cascade: str):
        self.CASCADE = cv2.CascadeClassifier(pfad_cascade)
        self.bildgroesse_output = 128
        self.counter = 0


    def setzeBildgroesse(self, bildgroesse_output):
        self.bildgroesse_output = bildgroesse_output


    def lade(self, pfad_video):
        self.pfad_video = pfad_video
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


    def fuerGesichterMache(self, funktion, max_anzahl_gesichter, speichern=True) -> int:
        if speichern:
            pfad_Video_ohne_Endung = ".".join(self.pfad_video.split(".")[:-1])
            video_writer = cv2.VideoWriter(f'{pfad_Video_ohne_Endung}_geändert.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_width, self.frame_height))

        ist_bild, bild = self.video.read()

        while ist_bild:
            bild_grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
            gesichter = self.CASCADE.detectMultiScale(bild_grau, scaleFactor=1.3, minNeighbors=5, minSize=(self.bildgroesse_output,)*2 )

            for (x, y, breite, hoehe) in gesichter:
                gesicht = bild[y:y+hoehe, x:x+breite]
                gesicht_skaliert = cv2.resize( gesicht, (self.bildgroesse_output,)*2 )
                rueckgabe_funktion = funktion( gesicht_skaliert )
                if type(rueckgabe_funktion) == bool and rueckgabe_funktion == False: break
                if speichern:
                    neues_Gesicht_skaliert = cv2.resize(rueckgabe_funktion, (breite, hoehe))
                    bild[y:y+hoehe, x:x+breite] = neues_Gesicht_skaliert
                    video_writer.write(bild)
                print("\r"+"Es wurden erfolgreich %d Bilder bearbeitet." % self.counter, end='')
                self.counter += 1

            ist_bild, bild = self.video.read()
            if self.counter >= max_anzahl_gesichter:
                break

        if speichern: video_writer.release()
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)
        x = self.counter
        self.counter = 0
        return x


    def extrahiereGesichter(self, max_anzahl_bilder: int, ordner_ausgabe: str):
        def funktion(bild):
            cv2.imwrite(os.path.join(ordner_ausgabe, f'Gesicht_{self.counter}.png'), bild)
            return True

        print("Exportiere Bilder nach %s." % ordner_ausgabe)
        anzahl_extrahierter_bilder = self.fuerGesichterMache(funktion, max_anzahl_bilder, speichern=False)
        print("\r"+"Es wurden erfolgreich %d Bilder nach %s exportiert." % (anzahl_extrahierter_bilder, ordner_ausgabe))


    def extrahiereUndValidiereGesichter(self, referenzbild: list, max_anzahl_bilder: int, ordner_ausgabe: str, toleranz=0.6):
        encoding_referenz = face_recognition.face_encodings(referenzbild)
        def funktion(bild):
            try:
                encoding_bild = face_recognition.face_encodings(bild)[0]
                if face_recognition.compare_faces(encoding_referenz, encoding_bild, tolerance=toleranz)[0]:
                    cv2.imwrite(os.path.join(ordner_ausgabe, f'Gesicht_{self.counter}.png'), bild)
                    return True
            except Exception: pass
            return False

        print("Validiere und exportiere Bilder nach %s." % ordner_ausgabe)
        anzahl_extrahierter_bilder = self.fuerGesichterMache(funktion, max_anzahl_bilder, speichern=False)
        print("\r"+"Es wurden erfolgreich %d Bilder nach %s exportiert." % (anzahl_extrahierter_bilder, ordner_ausgabe))


def main(argv):
    bildgroesse_ausgabe = 128
    max_anzahl_bilder = 50000
    pfad_cascade = "./daten/cascades/haarcascade_frontalface_default.xml"
    ordner_ausgabe = "./daten/Gesichter"
    pfad_validierungbild = ""
    toleranz = 0.6

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
            elif 'v' == argument[1]:
                pfad_validierungbild = argv[index+1]
            elif 't' == argument[1]:
                toleranz = float(argv[index+1])
            elif 'h' == argument[1]:
                print("Nutzung: %s [Optionen] [Videodatei]\n" % argv[0])
                print("""Optionen:
    -g : Größe der Ausgabe Bilder in Pixel
    -a : Maximale Anzahl der zu extrahierenden Bildern
    -c : Pfad für die Haarcascade
    -o : Zielordner für die Ausgabe
    -h : Drucken dieser Hilfenachricht
    -v : Pfad zu einem Validierungsbild
    -t : Toleranz für die Gesichtsvalidierung\n""")
                return

    g = Gesichterextrahierer(pfad_cascade)
    g.setzeBildgroesse(bildgroesse_ausgabe)
    g.lade(argv[-1])
    if pfad_validierungbild:
        validierungsbild = cv2.imread(pfad_validierungbild)
        g.extrahiereUndValidiereGesichter(validierungsbild, max_anzahl_bilder, ordner_ausgabe, toleranz=toleranz)
    else:
        g.extrahiereGesichter(max_anzahl_bilder, ordner_ausgabe)


if __name__ == "__main__":
    main(sys.argv)
