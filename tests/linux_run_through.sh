#!/bin/bash

path=./tests/
infile1=wayne-test-result
infile2=loveless-test-result

if ! python3 spectroart.py -t ; then
	cowsay "error in your program"
	exit
fi

if ! sox $path$infile1.wav -n spectrogram -o $path$infile1.png ; then
	exit
fi

if ! sox $path$infile2.wav -n spectrogram -o $path$infile2.png ; then
	exit
fi

xdg-open $path$infile1.png
xdg-open $path$infile2.png
