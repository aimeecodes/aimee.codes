with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "env";
  buildInputs = [
    zlib
    ruby.devEnv
    pkg-config
    bundix
    jekyll
  ];
}
