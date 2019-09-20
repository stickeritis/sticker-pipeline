#!/usr/bin/env python

import somajo
import sticker


class Pipeline:
    def __init__(self, config_files=[]):
        self._taggers = [
            sticker.Tagger(
                sticker.Config(config)) for config in config_files]

    def annotate_tokenized(self, sentences):
        for tagger in self.taggers:
            tagger.tag_sentences(sentences)

    @property
    def taggers(self):
        return self._taggers


class GermanPipeline(Pipeline):
    def __init__(self, config_files=[]):
        super().__init__(config_files)

        self._splitter = somajo.SentenceSplitter(is_tuple=False)
        self._tokenizer = somajo.Tokenizer(
            token_classes=False, extra_info=False)

    def annotate_text(self, text):
        tokens = self.tokenizer.tokenize_paragraph(text)
        sentences = list(map(lambda s: sticker.Sentence(s),
                             self.splitter.split(tokens)))
        self.annotate_tokenized(sentences)

        return sentences

    @property
    def splitter(self):
        return self._splitter

    @property
    def tokenizer(self):
        return self._tokenizer
