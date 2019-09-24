#!/usr/bin/env python

import somajo
import sticker

import sticker_workbench.cleanup as cleanup


class Pipeline:
    """A Sticker pipeline"""

    def __init__(self, config_files=[], cleanup=True):
        """
        Construct a sticker pipeline.

        Parameters
        ----------
        config_files : [str]
            The sticker configuration files of the models to load for
            the pipeline. The models will be applied in the given order.
        cleanup: bool, optional
            Replace non-ASCII punctuation by similar ASCII punctuation signs. 
        """
        
        self._cleanup = cleanup
        self._taggers = [
            sticker.Tagger(
                sticker.Config(config)) for config in config_files]

    def annotate_tokenized(self, sentences):
        """
        Annotate tokenized sentences.

        Parameters
        ----------
        sentences : [Sentence]
            The sentences to annotate. The sentences will be updated
            in-place.
        """
 
        for tagger in self.taggers:
            tagger.tag_sentences(sentences)

    @property
    def taggers(self):
        return self._taggers


class GermanPipeline(Pipeline):
    """A pipeline for German that tokenizes text using SoMaJo."""

    def __init__(self, config_files=[]):
        super().__init__(config_files)

        self._splitter = somajo.SentenceSplitter(is_tuple=False)
        self._tokenizer = somajo.Tokenizer(
            token_classes=False, extra_info=False)

    """
    Annotate a sentence.

    Parameters
    ----------
    sentence : str
        The sentence to tokenize and annotate.

    Returns
    -------
    Sentence
        The tokenized and annotated sentence.
    """
    def annotate_sentence(self, sentence):
        if self.cleanup:
            sentence = cleanup.cleanup(sentence)
        tokens = sticker.Sentence(self.tokenizer.tokenize(sentence))
        self.annotate_tokenized([tokens])
        return tokens

    """
    Annotate a text.

    Parameters
    ----------
    text : str
        The text to tokenize and annotate.

    Returns
    -------
    [Sentence]
        The tokenized and annotated sentences.
    """
    def annotate_text(self, text):
        if self.cleanup:
            text = cleanup.cleanup(text)

        tokens = self.tokenizer.tokenize_paragraph(text)
        sentences = list(map(lambda s: sticker.Sentence(s),
                             self.splitter.split(tokens)))
        self.annotate_tokenized(sentences)

        return sentences

    @property
    def cleanup(self):
        return self._cleanup

    @property
    def splitter(self):
        return self._splitter

    @property
    def tokenizer(self):
        return self._tokenizer
