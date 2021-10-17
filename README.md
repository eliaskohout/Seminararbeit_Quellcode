___
Das Projekt ist wie folgt strukturiert:

```
│
├── Deepfake.ipynb  
├── Gesichterextrahierer.py  
├── LoggingCallback.py  
├── README.md
├── daten  
│   ├── cascades  
│   │   └── haarcascade_frontalface_default.xml  
│   ├── lernen  
│   │   └── Gesichter
│   │       ├── A  
│   │       └── B  
│   └── modelle  
│       └── Autoencoder
│           ├── modell.info  
│           ├── Biden
│           │   ├── train.log
│           │   └── Gesichter
│           └── Norris
│               ├── train.log
│               └── Gesichter
└── skripte  
    ├── extrahiere_val_loss.awk  
    ├── frame_shuffle.py  
    ├── log_Analyse.awk
    └── plot.sh  
```

```📒 Deepfake.ipynb```   
_Das zentrale Jupyter Notebook, führe dies aus um ein künstliches Neuronales Netz zu erstellen und zu trainieren._

```🐍 Gesichterextrahierer.py```   
_Der Teil des Programms, der es ermöglicht Gesichter aus Videos auszuschneiden und zu manipulieren._

```🐍 LoggingCallback.py```  
_Ein Klasse, die dafür zuständig ist den Vortschritt während des Trainierens zu dokumentieren._

```📃 README.md```  
_Diese Datei._

```🧑🏼‍🦲 haarcascade_frontalface_default.xml```  
_Eine essenzielle Datei, die für das erkennen von Gesichtern im Gesichterextrahierer notwendig ist._

```📂 Gesichter```   
_In diesem Ordner werden in den Unterordnern A und B die Extrahierten Gesichter der Personen gespeichert, deren Gesichter ausgetauscht werden sollen. Diese Bilder werden dann zum Lernen verwendet._

```📂 modelle```   
_Hier werden, in einzelnen Unterordnern, die Modelle gespeichert. Wird einem Modell ein neuer Name gegeben, wird hier ein neuer Ordner erstellt._

```📂 Autoencoder```   
_Ein beispielhafter Ordner, der die Daten zu dem Modell mit dem Namen 'Autoencoder' enthält. Alle Dateien und Ordner, die hier enthalten sind werden automatisch generiert. Die Unterordner 'Biden' und 'Norris' enthalten jeweils einen Autoencoder, deren Namen zuvor gewählt werden kann._

```🪵 train.log```  
_Eine Textdatei, in der Lernfortschritt dokumentiert wird._

```📂 Bilder```   
_Im Laufe des Trainings werden immer wieder Bilder mit dem Modell erstellt, welche hier dann abgespeichert werden. Die Bilder, die ein 'A' im Namen haben, wurden mit dem Modell komprimiert und so ähnlich wie möglich wiederhergestellt. Die Bilder, die ein 'B' im Namen haben, wurden komprimiert und als die jeweils andere Person wiederhergestellt. Die Zahl im Namen ist die Unixzeit zu der das Bild entstanden ist._

```ℹ️ modell.info```  
_Eine Textdatei mit einer Übersicht über die Struktur des Modells._

```📂 skripte```   
_Ein Ordner, der ein paar hilfreich Hilfsprogramme enthält._

```📄 extrahiere_val_loss.awk```   
_Ein AWK-Skript, dass eine train.log-Datei einliest und eine Liste an Zeitpunkten mit dem passenden Fehlerwert zurückgibt. Es wird für die plot.sh-Datei benötigt._

```🐍 frame_shuffle.py```  
_Ein Python-Programm, dass die Bilder in einem Video mischt._

```📄 log_Analyse.awk```   
_Ein AWK-Skript, dass eine übergebene train.log-Datei analysiert und eine Zusammenfassung über den Trainingsverlauf gibt._

```💲 plot.sh```  
_Ein Bash-Skript, dass aus einer oder mehreren übergebenen train.log-Dateien einen Diagramm erstellt._
