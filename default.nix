with import <nixpkgs> {};
mkShell {
  nativeBuildInputs = [
    python313
    python313Packages.pygame
  ];
}
