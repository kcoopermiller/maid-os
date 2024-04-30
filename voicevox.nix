{ system ? builtins.currentSystem, pkgs ? import <nixpkgs> { inherit system; }, lib, stdenv, fetchurl, autoPatchelfHook, ffmpeg, glib, glibc, nss, gtk3
, nspr, cups, dbus, libdrm, pango, cairo, xorg, mesa, expat, libxkbcommon
, alsa-lib, at-spi2-atk, portaudio, gcc_debug
}:
let
  pkgs = import (builtins.fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/50a7139fbd1acd4a3d4cfa695e694c529dd26f3a.tar.gz";
    sha256="1rh75qfcdbczm2rdzqni21xj0wc8f92mhnpwq5mv3z0yy8f35krl";
  }) { inherit system; };
  onnxruntime_1_13_1 = pkgs.onnxruntime;
in
stdenv.mkDerivation rec {
  pname = "voicevox";
  version = "0.18.1";

  src = fetchurl {
    url = "https://github.com/VOICEVOX/voicevox/releases/download/${version}/voicevox-linux-cpu-${version}.tar.gz";
    sha256 = "FCAfMym5XIBi7PrFDDyVF4TfphItk8/Tbfag0VS7yy0=";
  };

  nativeBuildInputs = [
    autoPatchelfHook
  ];

  buildInputs = [
    # ffmpeg
    glib
    glibc
    nss
    gtk3
    nspr
    cups
    dbus
    libdrm
    pango
    cairo
    xorg.libX11
    xorg.libXcomposite
    xorg.libXdamage
    xorg.libXext
    xorg.libXfixes
    xorg.libXrandr
    xorg.libxcb
    mesa
    expat
    libxkbcommon
    alsa-lib
    at-spi2-atk
    portaudio
    gcc_debug
    onnxruntime_1_13_1
    stdenv.cc.cc.lib
  ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    mkdir -p $out/lib

    tar -xzvf $src

    extracted_dir=$(find . -maxdepth 1 -type d -name "VOICEVOX")

    cp -r $extracted_dir/* $out/bin/
    rm $out/bin/lib*
    # rm $out/bin/vv-engine/lib* 
    cp $extracted_dir/lib* $out/lib/
    cp -r $extracted_dir/vv-engine/lib* $out/lib/

    runHook postInstall  
  '';

  meta = with lib; {
    homepage = "https://voicevox.hiroshiba.jp/";
    # Dual license of LGPL v3 and another license that does not require publication of source code
    license = [ licenses.lgpl3 licenses.unfree ];
    description = "The engine for VoiceVox, an OS text-to-speech synthesizer software developed by Hiho";
    platforms = platforms.linux;
  };
}
