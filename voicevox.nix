{ lib, stdenv, fetchurl, glib, glibc, nss, autoPatchelfHook, gtk3
, nspr, cups, dbus, libdrm, pango, cairo, xorg, mesa, expat, libxkbcommon
, alsa-lib, at-spi2-atk, portaudio, gcc_debug
}:

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
    stdenv.cc.cc.lib
  ];
  

  installPhase = ''
    ls $src
    runHook preInstall
    install -m755 -D $src $out/bin/voicevox
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
