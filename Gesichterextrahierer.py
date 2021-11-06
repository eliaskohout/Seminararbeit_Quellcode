<<<<<<< HEAD
#!python3.8
=======
#!/usr/bin/python3

"""
Ein Skript das sowohl als eigenständiges Programm genutzt werden kann, als auch als 
Modul importiert werden kann. Ermöglicht das Extrahieren und bearbeiten von Gesichtern 
in Videos.

Nutzung als Modul:
1. Mit dem Pfad zur Kaskade initalisieren.
2. Optional die Bildergröße der Ausgabe mit 'setzeBildergroesse' setzen.
3. Video laden mit 'lade'.
4. Video mit den anderen Methoden
    - fürGesichterMache
    - extrahiereGesichter
    - extrahiereUndValidiereGesichter
        bearbeiten.

Nutzung als Skript:
-> Mit Python3 und der '-h' Option starten um die Hilfe angezeigt zu bekommen.
"""

>>>>>>> 61d813d3919bfc21a299729d689a1889eeedcd70
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
        """
        Spielt das geladene Video in einem neuen Fenster ab. Escape beendet die Wiedergabe.
        """
        while True:
            ist_bild, bild = self.video.read()  # Nächsten Frame einlesen
            if cv2.waitKey(1) == 27 or not ist_bild:
                break
            cv2.imshow('Deepfakeskript - Video', bild)
            time.sleep(1/self.fps-1)
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Video zurücksetzen, damit es wieder eingelesen werden kann
        cv2.destroyAllWindows()


    def fuerGesichterMache(self, funktion, max_anzahl_gesichter, speichern=True) -> int:
        """
        Fürt die übergebene Funktion für alle Gesichter in dem Video aus. Es werden maximal ein Gesicht pro Bild erkannt.


        :funktion: Eine Funktion, der beim Ausführen ein Parameter, der Bildausschnitt des Gesichts, als Liste übergeben wird.
                    Gibt die Funktion False zurück wird das gerade bearbeitete Bild übersprungen.
                    Gibt die Funktion True wird der Counter erhöht und das nächste Bild geladen, sofern nicht das Maximum erreicht wurde.
                    Gibt die Funktion ein Bild als Liste zurück, wird dies anstelle des übergebenen Gesichts in das Bild des Videos eingesetzt. Das Ein- und Ausgabeliste muss die gleiche Form haben.
                    Es kann von der Funktion aus `self.counter` zugegriffen werden, um die Anzahl an bearbeiteten Bildern zu erhalten.
        :max_anzahl_gesichter: Definiert die Anzahl an Gesichtern, die maximal bearbeitet werden. Die Funktion endet vorzeitig wenn die Videodatei zu Ende ist.
        :speichern: Bei True wird eine Videodatei abgespeichert, die die mögliche Änderungen beinhaltet.
                    Bei False ist dies nicht der Fall.
        :return: Gibt die Anzahl an bearbeiteten Bildern zurück.
        """
        if speichern:  # Vorbereitung für das Abspeichern des neuen Videos
            pfad_Video_ohne_Endung = ".".join(self.pfad_video.split(".")[:-1])
            video_writer = cv2.VideoWriter(f'{pfad_Video_ohne_Endung}_geändert.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_width, self.frame_height))

        ist_bild, bild = self.video.read() # Ersten Frame einlesen

        while ist_bild:  # Solange das Video nicht zu Ende ist
            bild_grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
<<<<<<< HEAD
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
=======
            gesichter = self.CASCADE.detectMultiScale(bild_grau, scaleFactor=1.3, minNeighbors=5, minSize=(self.bildgroesse_output,)*2 )  # Gesichter erkennen

            if gesichter:
                x, y, breite, hoehe = gesichter[0]  # Bearbeitet nur das erste Gesicht
                gesicht = bild[y:y+hoehe, x:x+breite]  # Kopieren des Gesichts
                gesicht_skaliert = cv2.resize( gesicht, (self.bildgroesse_output,)*2 ) 
                rueckgabe_funktion = funktion( gesicht_skaliert )  # Die übergebene Funktion ausführen
                if rueckgabe_funktion == False: break  # Mit dem nächsten Frame fortfahren
                if speichern:
                    if rueckgabe_funktion != True:
                        bild[y:y+hoehe, x:x+breite] = rueckgabe_funktion  # Rückgabe der Funktion in das Bild einsetzen
                    video_writer.write(bild)  # Frame an das neue Video anhängen
>>>>>>> 61d813d3919bfc21a299729d689a1889eeedcd70
                print("\r"+"Es wurden erfolgreich %d Bilder bearbeitet." % self.counter, end='')
                self.counter += 1
            elif speichern:
                video_writer.write(bild)  # Frame an das neue Video anhängen auch wenn kein Gesicht gefunden wurde

            ist_bild, bild = self.video.read()  # Nächsten Frame einlesen
            if self.counter >= max_anzahl_gesichter:
                break

        if speichern: video_writer.release()
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Video zurücksetzen, damit es wieder eingelesen werden kann
        x = self.counter
        self.counter = 0
        return x


<<<<<<< HEAD
    def extrahiereGesichter(self, max_anzahl_bilder: int, ordner_ausgabe: str):
=======
    def extrahiereGesichter(self, max_anzahl_gesichter: int, ordner_ausgabe: str):
        """
        Findet alle Gesichter aus dem Video und speichert sie ab.

        :max_anzahl_gesichter: Definiert die Anzahl an Gesichtern, die maximal bearbeitet werden. Die Funktion endet vorzeitig wenn die Videodatei zu Ende ist.
        :ordner_ausgabe: Den Pfad zum Ordner in dem die Bilder abgespeichert werden, dieser muss vorhanden sein.
        """
>>>>>>> 61d813d3919bfc21a299729d689a1889eeedcd70
        def funktion(bild):
            cv2.imwrite(os.path.join(ordner_ausgabe, f'Gesicht_{self.counter}.png'), bild)
            return True

        print("Exportiere Bilder nach %s." % ordner_ausgabe)
        anzahl_extrahierter_bilder = self.fuerGesichterMache(funktion, max_anzahl_gesichter, speichern=False)
        print("\r"+"Es wurden erfolgreich %d Bilder nach %s exportiert." % (anzahl_extrahierter_bilder, ordner_ausgabe))


<<<<<<< HEAD
    def extrahiereUndValidiereGesichter(self, referenzbild: list, max_anzahl_bilder: int, ordner_ausgabe: str, toleranz=0.6):
=======
    def extrahiereUndValidiereGesichter(self, referenzbild: list, max_anzahl_gesichter: int, ordner_ausgabe: str, toleranz=0.6):
        """
        Findet alle Gesichter aus dem Video und speichert sie ab, falls sie dem Referenzgesicht ausreichend ähneln.

        :referenzbild: Ein Bild in Form einer Liste das zum Vergleich bei der Validierung verwendet wird.
        :max_anzahl_gesichter: Definiert die Anzahl an Gesichtern, die maximal bearbeitet werden. Die Funktion endet vorzeitig wenn die Videodatei zu Ende ist.
        :ordner_ausgabe: Den Pfad zum Ordner in dem die Bilder abgespeichert werden, dieser muss vorhanden sein.
        :toleranz: Die euklidische Distanz, die maximal zwischen den Vekoren, die die zu vergleichenden Gesichter repräsentieren,
                liegen darf, damit diese als von der gleichen Person gelten. (siehe face_recongnition.compare_faces)
        """
>>>>>>> 61d813d3919bfc21a299729d689a1889eeedcd70
        encoding_referenz = face_recognition.face_encodings(referenzbild)
        def funktion(bild):
            try:
                encoding_bild = face_recognition.face_encodings(bild)[0]  # Gesicht in ein Vektorrepräsentation umwandeln
                if face_recognition.compare_faces(encoding_referenz, encoding_bild, tolerance=toleranz)[0]:
                    cv2.imwrite(os.path.join(ordner_ausgabe, f'Gesicht_{self.counter}.png'), bild)
                    return True
            except Exception: pass
            return False

        print("Validiere und exportiere Bilder nach %s." % ordner_ausgabe)
        anzahl_extrahierter_bilder = self.fuerGesichterMache(funktion, max_anzahl_gesichter, speichern=False)
        print("\r"+"Es wurden erfolgreich %d Bilder nach %s exportiert." % (anzahl_extrahierter_bilder, ordner_ausgabe))


def main(argv):  # Wird ausgeführt, wenn das Skript direkt ausgeführt wird
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
