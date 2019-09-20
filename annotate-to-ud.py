#!/usr/bin/env python

import argparse
import sys

from pipeline import GermanPipeline

parser = argparse.ArgumentParser(description='Sticker pipelines.')
parser.add_argument('models', metavar='MODEL', type=str, nargs='*',
                    help='a model in the pipeline')

if __name__ == "__main__":
    args = parser.parse_args()

    pipeline = GermanPipeline(args.models)

    for line in sys.stdin:
        sentences = pipeline.annotate_text(line.strip())

        for sentence in sentences:
            for (idx, token) in enumerate(sentence):
                if idx == 0:
                    continue

                if token.pos is not None:
                    pos_parts = token.pos.split("-")
                    upos = pos_parts[0]
                    xpos = pos_parts[1]
                else:
                    xpos = upos = "_"

                if token.head is not None:
                    head = token.head
                else:
                    head = "_"

                if token.head_rel is not None:
                    head_rel = token.head_rel
                else:
                    head_rel = "_"

                print(
                    "%d\t%s\t_\t%s\t%s\t_\t%s\t%s\t_\t_" %
                    (idx, token.form, upos, xpos, head, head_rel))
            print()
