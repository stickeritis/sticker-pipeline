{ callPackage, fetchFromGitHub, nix-gitignore, python3Packages }:

let
  danieldk = callPackage (builtins.fetchTarball {
    url = "https://git.sr.ht/~danieldk/nix-packages/archive/7049128b270cd15858c41ba0464f0444e25dce2e.tar.gz";
    sha256 = "183y7y327r4v49qwi0prf9qyfj8qzd0z3hbxh7mcaa0k3cm5sck5";
  }) {};
  sticker = callPackage (fetchFromGitHub {
    owner = "stickeritis";
    repo = "nix-packages";
    rev = "4a2e5c8ff801d5fb1754054ecf85764b6a7d9c82";
    sha256 = "1n4i3hgbs1qv2s5gdaw73m46svsp8l3x3s5vl5lxg6h0nd5mpfg1";
  }) {};
  sticker-python = callPackage (fetchFromGitHub {
    owner = "stickeritis";
    repo = "sticker-python";
    rev = "98a1820a04cd58ec97edcfcf88b2fc038311511b";
    sha256 = "01vn2kvmcw1n8945xirccqhr8vmdlq3rlz1wcvkdnrcp06hrl9s9";
  }) {};
in python3Packages.buildPythonApplication rec {
  pname = "sticker-workbench";
  version = "0.1.0";

  src = nix-gitignore.gitignoreSource [ ".git/" "*.nix" "/nix" ] ./.;

  propagatedBuildInputs = [
    danieldk.python3Packages.somajo
    sticker-python
  ];

  checkInputs = with python3Packages; [
    pytest
  ];

  checkPhase = ''
    pytest
  '';
}
