with import <nixpkgs> {};

let
  sticker = callPackage (fetchFromGitHub {
    owner = "stickeritis";
    repo = "nix-packages";
    rev = "b25beaa717fd7ecc2fa309101bd31ca6635caba7";
    sha256 = "0sqcsk2x41z0i5253jsvvxchr77c4d86jzcvng5s726gpvycv85a";
  }) {};
  sticker-python = callPackage (fetchFromGitHub {
    owner = "stickeritis";
    repo = "sticker-python";
    rev = "f6caca08f23e2ea5873fc02509beef6fed27f13b";
    sha256 = "1ix90xhk4s2z1xc6mvwvqmghhwdphgxk2yyq2kgdc1lxhwmzc9sc";
  }) {};
in stdenv.mkDerivation rec {
  name = "pipeline-env";
  env = buildEnv { name = name; paths = buildInputs; };

  buildInputs = [
    sticker.models.de-pos-ud.model
    sticker.models.de-deps-ud-small.model

    qt5.qtbase

    sticker-python
    nlp.python3Packages.somajo
    python3Packages.pyqt5
    python3Packages.pyqtwebengine
  ];

  nativeBuildInputs = [
  ];

  # Normally set by the wrapper, but we can't use it in nix-shell (?).
  QT_QPA_PLATFORM_PLUGIN_PATH="${qt5.qtbase.bin}/lib/qt-${qt5.qtbase.version}/plugins";
  POS_MODEL="${sticker.models.de-pos-ud.model}/share/sticker/models/de-pos-ud/sticker.conf";
  DEPS_MODEL="${sticker.models.de-deps-ud-small.model}/share/sticker/models/de-deps-ud-small/sticker.conf";
  NER_MODEL="${sticker.models.de-ner-ud-small.model}/share/sticker/models/de-ner-ud-small/sticker.conf";
}
