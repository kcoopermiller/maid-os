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
        # voicevox = pkgs.callPackage ./voicevox.nix { inherit pkgs system; };
       in {
        devShell = pkgs.mkShell {
          venvDir = "./.venv";
          buildInputs = with pkgs; [
            cava
            scrot
            xclip
            stdenv.cc.cc.lib
            tesseract
            xorg.libX11
            xorg.libXrandr
            cudaPackages.cudatoolkit
            cudaPackages.cudnn
            pythonPackages.opencv4
            pythonPackages.dbus-python
            pythonPackages.venvShellHook
            pythonPackages.pytorch-bin
            pythonPackages.torchaudio-bin
            pythonPackages.python-dotenv
            pythonPackages.pyautogui
            pythonPackages.plyer
            pythonPackages.pytesseract
            pythonPackages.pyperclip
            pythonPackages.numpy
            pythonPackages.sounddevice
            pythonPackages.screeninfo
            docker
            docker-compose
          ];

          postVenvCreation = ''
            unset SOURCE_DATE_EPOCH
            pip install -r requirements.txt
          '';

          postShellHook = ''
            # allow pip to install wheels
            unset SOURCE_DATE_EPOCH
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
            docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
            docker run -d --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
          '';
        };
      }
    );
}
