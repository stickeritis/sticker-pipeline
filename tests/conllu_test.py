from sticker import Sentence
from sticker_workbench.conllu import sentence_to_conllu

def test_sentence_to_conll():
    sent = Sentence(["Hans", "rennt", "heute"], ["DET-DET", "V-VFIN", "ADV-ADV"])
    sent[1].features["NE"] = "Person"
    sent[1].features["tf"] = "VF"
    sent[2].features["tf"] = "LK"
    sent[3].features["tf"] = "MF"

    # We currently have no way of setting a head/dependent, so
    # unfortunately we cannot test this yet.
    assert sentence_to_conllu(sent) == """1	Hans	_	DET	DET	NameType=Person|TopoField=VF	_	_	_	_
2	rennt	_	V	VFIN	TopoField=LK	_	_	_	_
3	heute	_	ADV	ADV	TopoField=MF	_	_	_	_"""
