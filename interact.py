#!/usr/bin/env python

import argparse
import atexit
import os
from multiprocessing import Process, Pipe
import readline
import sys


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from pipeline import GermanPipeline
from ud import sentencesToUD
from visualizer import Visualizer

parser = argparse.ArgumentParser(description='Sticker pipelines.')
parser.add_argument('models', metavar='MODEL', type=str, nargs='*',
                    help='a model in the pipeline')

lastSentences = None

global visualizer
visualizer = None

def show_annotations(sentences):
    def show(pipeline):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app = QApplication(sys.argv)
        visualizer = Visualizer()
        visualizer.displaySentences(sentences)

    p = Process(target=show, args=(sentences,))
    p.start()

    return p

def process(pipeline, command):
    global lastSentences
    if command == "t" or command == "tree":
        show_annotations(sentencesToUD(lastSentences))
    elif command.startswith("p "):
        lastSentences = pipeline.annotate_text(command[2:])

if __name__ == "__main__":
    args = parser.parse_args()

    pipeline = GermanPipeline(args.models)

    histfile = os.path.join(os.path.expanduser("~"), ".sticker_history")
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    readline.parse_and_bind('tab: complete')

    atexit.register(readline.write_history_file, histfile)

    try:
        while True:
            command = input('-> ').strip()
            process(pipeline, command)
    except (EOFError, KeyboardInterrupt) as e:
        print('\nBye bye...')
