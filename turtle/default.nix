with import <nixpkgs> {};
let
  pythonEnv = pkgs.python313.withPackages (ps: [
    # ps.pygame
    ps.tkinter
  ]);
in
mkShell {
  nativeBuildInputs = [
      pythonEnv
  ];
}
