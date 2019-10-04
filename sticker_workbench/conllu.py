def extract_features(token):
    # Feature iteration is not yet possible in sticker-python,
    # so probe for specific features.
    features = []
    if token.features.contains("NE"):
        ne = token.features["NE"]
        if ne != "O":
            features.append("NameType=%s" % strip_iob(ne))

    if token.features.contains("tf"):
        features.append("TopoField=%s" % token.features["tf"])

    if len(features) == 0:
        return "_"
    else:
        return "|".join(features)


def strip_iob(tag):
    if tag.startswith("I-"):
        return tag[2:]
    if tag.startswith("B-"):
        return tag[2:]

    return tag


def sentences_to_conllu(sentences):
    """Convert multiple sentences to CoNLL-U"""

    return "\n\n".join(map(lambda s: sentence_to_conllu(s), sentences))


def sentence_to_conllu(sentence):
    """Convert multiple sentences to CoNLL-U"""

    lines = []

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
            head = str(token.head)
        else:
            head = "_"

        if token.head_rel is not None:
            head_rel = token.head_rel
        else:
            head_rel = "_"

        features = extract_features(token)

        lines.append(
            "%d\t%s\t_\t%s\t%s\t%s\t%s\t%s\t_\t_" %
            (idx, token.form, upos, xpos, features, head, head_rel))

    return '\n'.join(lines)
