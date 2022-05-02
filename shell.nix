{ pkgs ? import <nixpkgs> {} }:
let
  py-w-pkgs = pkgs.python310.withPackages (p: with p; [
    pytelegrambotapi
  ]);
in
pkgs.mkShell {
  buildInputs = [
    py-w-pkgs
  ];
  shellHook = ''
    PYTHONPATH=${py-w-pkgs}/${py-w-pkgs.sitePackages}
  '';
}
