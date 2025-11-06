from scipy.signal import ShortTimeFFT
import soundfile as sf
from PIL import Image
import numpy as np
import timeit
import sys

# Check parameters
if len(sys.argv) != 2:
    print("Usage: proto.py infile")
    exit()

t1 = timeit.default_timer()

infile = sys.argv[1]

print(f"Processing {infile}")

im = Image.open(infile)
# Load pixel data
pix = im.load() 

width, height = im.size

fs = 44100

# Window length is 2 x image height because
# bin[x] = bin[-x] when x < image height
win_len = 2*height - 1

# STFT series is generated here
series = [[] for _ in range(height)]

for y in range(height):
    for x in range(width):
        normalized = np.array(pix[x, height - 1 - y]) / 255 # Normalize pixel values to range 0.0 - 1.0
        normalized *= [0.5, 1, 0.25]                        # Apply weights to rgb values
        avg = np.sum(normalized) / 3
        brightness = avg**2                                 # Easy way to add contrast to brightness values
        series[y].append(brightness)

series = np.array(series)

SFT = ShortTimeFFT(win=np.hanning(win_len),
                   hop=(height),
                   fs=fs)

# Create audio with inverse STFT
audio_picture = SFT.istft(series)

# Normalize output
audio_picture /= np.max(np.abs(audio_picture))

outfile = infile.split('.')[0] + ".wav"

sf.write(outfile, audio_picture, fs)

t2 = timeit.default_timer()
dur = t2 - t1

print(f"Output written to {outfile} in {dur:.2f} seconds")
