from sticker_workbench.pipeline import GermanPipeline

# Only test basic tokenization, since we do not have models
# available (yet).


def test_german_pipeline():
    pipeline = GermanPipeline()
    annotations = pipeline.annotate_text(
        "Sowohl Luciferine als auch Luciferasen sind art- oder taxonspezifisch, also für jede Lebewesengruppe kennzeichnend. Die Spannweite der emittierten Farbe befindet sich zwischen blauem und rotem Licht")
    forms = [list(map(lambda t: t.form, sentence)) for sentence in annotations]
    assert forms == [[None,
                      'Sowohl',
                      'Luciferine',
                      'als',
                      'auch',
                      'Luciferasen',
                      'sind',
                      'art-',
                      'oder',
                      'taxonspezifisch',
                      ',',
                      'also',
                      'für',
                      'jede',
                      'Lebewesengruppe',
                      'kennzeichnend',
                      '.'],
                     [None,
                      'Die',
                      'Spannweite',
                      'der',
                      'emittierten',
                      'Farbe',
                      'befindet',
                      'sich',
                      'zwischen',
                      'blauem',
                      'und',
                      'rotem',
                      'Licht']]
