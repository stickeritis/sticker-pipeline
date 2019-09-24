from sticker_workbench.cleanup import cleanup


def test_cleanup_fixes_punctuation():
    assert cleanup(
        '„Wir wissen es noch nicht“, sagt er') == '"Wir wissen es noch nicht", sagt er'
