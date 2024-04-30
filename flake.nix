{
  description = "Maid OS Development Environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { 
          inherit system; 
          config.allowUnfree = true; 
          # config.cudaSupport = true;
        };
        pythonPackages = pkgs.python3Packages;

        voicevox-client = pythonPackages.buildPythonPackage rec {
          pname = "voicevox-client";
          version = "0.4.1";
          src = pythonPackages.fetchPypi {
            inherit pname version;
            sha256 = "sha256-71c1rFw0r4VzOnr6iN8PAeCRuQWxvFD+CsAncdyUgKo=";
          };
           build-system = [
             pythonPackages.setuptools
             pythonPackages.wheel
           ];
        };
        voicevox = pkgs.callPackage ./voicevox.nix { inherit pkgs system; };
       in {
        devShell = pkgs.mkShell {
          venvDir = "./.venv";
          buildInputs = with pkgs; [
            voicevox
            cava
            scrot
            stdenv.cc.cc.lib
            cudaPackages.cudatoolkit
            cudaPackages.cudnn
            pythonPackages.venvShellHook
            pythonPackages.pytorch-bin
            pythonPackages.torchaudio-bin
            # pythonPackages.open-interpreter
            # pythonPackages.groq
            pythonPackages.python-dotenv
            pythonPackages.pyautogui
            # pythonPackages.opencv-python
            pythonPackages.plyer
            pythonPackages.pyperclip
            # pythonPackages.PyWinCtl
            # pythonPackages.voicevox-client
            pythonPackages.numpy
            pythonPackages.sounddevice
            # voicevox-client
          ];

          postVenvCreation = ''
            unset SOURCE_DATE_EPOCH
            pip install -r requirements.txt
          '';

          postShellHook = ''
            # allow pip to install wheels
            unset SOURCE_DATE_EPOCH
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
          '';
        };
      }
    );
}
