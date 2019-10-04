{ callPackage, fetchFromGitHub, nix-gitignore, python3Packages }:

let
  danieldk = callPackage (builtins.fetchTarball {
    url = "https://git.sr.ht/~danieldk/nix-packages/archive/7049128b270cd15858c41ba0464f0444e25dce2e.tar.gz";
    sha256 = "183y7y327r4v49qwi0prf9qyfj8qzd0z3hbxh7mcaa0k3cm5sck5";
  }) {};
  sticker = callPackage (fetchFromGitHub {
    owner = "stickeritis";
    repo = "nix-packages";
    rev = "2a0192f2ae5b2aff7961c1b90dad5abfb5c827d5";
    sha256 = "1vsz8hy1dj465g0ng87n5wm2hdjxpw1q62lgjxb8k1rqb1gp3mv9";
  }) {};
in python3Packages.buildPythonApplication rec {
  pname = "sticker-workbench";
  version = "0.1.0";

  src = nix-gitignore.gitignoreSource [ ".git/" "*.nix" "/nix" ] ./.;

  propagatedBuildInputs = [
    danieldk.python3Packages.somajo
    sticker.python3Packages.sticker
  ];

  checkInputs = with python3Packages; [
    pytest
  ];

  checkPhase = ''
    pytest
  '';
}
