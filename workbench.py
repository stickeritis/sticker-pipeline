#!/usr/bin/env python

import argparse
import atexit
import os
from multiprocessing import Process, Pipe
import readline
import sys


from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication


from sticker_workbench.pipeline import GermanPipeline
from sticker_workbench.visualizer import Visualizer
from sticker_workbench.conllu import sentences_to_conllu

parser = argparse.ArgumentParser(description='Sticker pipelines.')
parser.add_argument('models', metavar='MODEL', type=str, nargs='*',
                    help='a model in the pipeline')

lastSentences = None

class Emitter(QThread):
    display = pyqtSignal(str)
    stop = pyqtSignal()

    def __init__(self, pipeline):
        super(Emitter, self).__init__()
        self._pipeline = pipeline

    def run(self):
        while True:
            try:
                ud = self.pipeline.recv()
                if ud is None:
                    break
                else:
                    self.display.emit(ud)
            except EOFError:
                break

        self.stop.emit()

    @property
    def pipeline(self):
        return self._pipeline

visualizer_process = None
visualizer_pipeline = None

def create_visualizer():
    global visualizer_process
    global visualizer_pipeline

    def run_visualizer(pipeline):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app = QApplication(sys.argv)
        visualizer = Visualizer()

        emitter = Emitter(pipeline)
        emitter.display.connect(visualizer.setSentences)
        emitter.stop.connect(visualizer.stop)
        emitter.start()

        visualizer.run()

    # Cleanup dead visualizer process.
    if visualizer_process is not None and not visualizer_process.is_alive():
        visualizer_process.join()
        visualizer_process = None

    # Set up visualizer process
    if visualizer_process is None:
        visualizer_pipeline, slave_pipeline = Pipe()
        visualizer_process = Process(target=run_visualizer, args=(slave_pipeline,))
        visualizer_process.start()

def print_triples():
    if lastSentences is None:
        return

    for (sentence_idx, sentence) in enumerate(lastSentences):
        if sentence_idx != 0:
            print()
        for idx, token in enumerate(sentence):
            if idx == 0:
                continue

            if token.head is None or token.head_rel is None:
                continue

            print("%s/%d %s-> %s/%d" % (sentence[token.head].form, token.head, token.head_rel, token.form, idx))

def process(pipeline, command):
    global lastSentences
    parts = command.split(" ", 1)
    command = parts[0].strip()
    if len(parts) == 2:
        arg = parts[1].strip()
    else:
        arg = None

    if command == "t" or command == "tree":
        if lastSentences is None:
            print("There is nothing to visualize")
        else:
            create_visualizer()
            visualizer_pipeline.send(sentences_to_conllu(lastSentences))
    elif command == "p":
        if arg is None:
            print("p requires an argument")
            return
        lastSentences = pipeline.annotate_text(arg)
    elif command == "triples":
        print_triples()

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

    if visualizer_process.is_alive():
        visualizer_pipeline.send(None)
        visualizer_process.join()
