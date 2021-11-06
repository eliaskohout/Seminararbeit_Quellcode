#!/usr/bin/python3

"""
Ein simples Skript, das es ermöglicht die Bilder in einem Video zu mischen.
Wenn die Datei direkt als Skript ausgeführt wird, wird das erste Argument als Pfad für das zu bearbeitende Video verwendet.
"""

import cv2, sys, random, time

def shuffle(pfad_video):
    video = cv2.VideoCapture(pfad_video)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

    pfad_video_ohne_endung = '.'.join(pfad_video.split('.')[:-1])

    video_writer = cv2.VideoWriter(f'{pfad_video_ohne_endung}_gemischt.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    frame_num_liste = list(range(1, frame_count+1))
    random.shuffle(frame_num_liste)

    startzeit = time.time()
    for ind, val in enumerate(frame_num_liste):
        if ind%30 == 0:
            verbleibende_min = ( (time.time()-startzeit)/(ind+1) )*( frame_count-ind )/60
            print(f"\rFortschritt: {int(ind/frame_count*100)}%, geschätzte verbleibende Zeit: {verbleibende_min:.2f} Minuten", end='')
        video.set(cv2.CAP_PROP_POS_FRAMES, val)
        ist_bild, bild = video.read()
        video_writer.write(bild)

    video.release()
    video_writer.release()


if __name__ == '__main__':
    shuffle(sys.argv[1])
