import sys
import numpy as np
from PIL import Image
from scipy.signal import istft, windows
import soundfile as sf

if len(sys.argv) != 2:
    print("Usage: python proto-juho.py <imagefile>")
    sys.exit(1)

infile = sys.argv[1]

# Load image:

im = Image.open(infile).convert("RGB")
width, height = im.size
pix = np.asarray(im, dtype=float) / 255.0  # (height, width, rgb)


# Parameters:
fs = 44100
nperseg = 2 * height - 1 # window length

# RBG Brightness conversion:
weights = np.array([0.5, 1.0, 0.25])
brightness = np.dot(pix, weights) / weights.sum()
brightness = np.power(brightness, 2.5) # contrast (will make bright pixels more bright)
brightness = brightness[::-1, :] # flip image

# Apply brightness and Hann window:
random_phase = np.exp(1j * 2 * np.pi * np.random.rand(*brightness.shape))
spectro = brightness * windows.hann(height, sym=False)[:, None] * random_phase

# ISTFT
_, audio = istft(spectro,fs=fs,nperseg=nperseg)

# Normalization:
audio = np.real(audio)
audio /= np.max(np.abs(audio))

# Write output file
outfile = infile.split('.')[0] + ".wav"
sf.write(outfile, audio, fs)


print(f"Output: {outfile}")