
with (import <nixpkgs> {});
let
  env = bundlerEnv {
    name = "aimee.codes";
    inherit ruby;
    gemfile = ./Gemfile;
    lockfile = ./Gemfile.lock;
    gemset = ./gemset.nix;
  };

in stdenv.mkDerivation {
  name = "aimee.codes";
  buildInputs = [env ruby];
}
