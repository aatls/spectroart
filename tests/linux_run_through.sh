#!/bin/bash

if ! python3 spectroart.py -t ; then
	cowsay "error in your program"
	exit
fi

if ! sox test-result.wav -n spectrogram ; then
	exit
fi

xdg-open spectrogram.png

