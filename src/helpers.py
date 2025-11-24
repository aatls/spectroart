import soundfile as sf
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import matplotlib.colors as mcolors

def write_audio(outfile, data, samplerate):
    sf.write(outfile, data, samplerate)
    
def load_image(infile):
    image = Image.open(infile).convert("RGB")
    return image

def resize_array(input, new_length):
    """Resizes input array with linear interpolation"""

    output = np.empty(new_length)

    ratio = (len(input) - 1) / (new_length - 1)

    output[0] = input[0]

    for out_i in range(1, new_length - 1):
        in_i = out_i * ratio
        offset = in_i - int(in_i)

        new_val = input[int(in_i)] * (1 - offset) + input[int(in_i) + 1] * offset
        output[out_i] = new_val

    output[-1] = input[-1]

    return output

def spectrogramify(data, samplerate, min_f, max_f):

    if data.ndim == 2:
        data = data.mean(axis=1)
        
    # Compute spectrogram
    nperseg = 4096/2
    noverlap = int(nperseg * 0.875)  # 87.5% overlap
    window = np.hanning(nperseg)


    frequencies, times, Sxx = signal.spectrogram(
        data,
        fs=samplerate,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        scaling='density',
        mode='psd'
    )

    # Convert to dB relative to the maximum (so max becomes 0 dB)
    eps = 1e-12
    Sxx_db = 10.0 * np.log10(Sxx + eps)
    Sxx_db -= Sxx_db.max()

    range_db = 60 #or something
    Sxx_db = np.clip(Sxx_db, -range_db, 0.0)

    freq_mask = (frequencies >= min_f) & (frequencies <= max_f)
    frequencies_f = frequencies[freq_mask]
    Sxx_db_f = Sxx_db[freq_mask, :]

    cdict = {
        'red':   [(0.0, 0.0, 0.0),    # -100 dB → dark blue
                (0.3, 0.5, 0.5),    # around -70 dB → blue-magenta
                (0.5, 1.0, 1.0),    # around -50 dB → magenta/red
                (0.75, 1.0, 1.0),   # around -25 dB → red/white
                (1.0, 1.0, 1.0)],   # 0 dB → white

        'green': [(0.0, 0.0, 0.0),
                (0.3, 0.0, 0.0),
                (0.5, 0.0, 0.0),
                (0.75, 0.5, 0.5),
                (1.0, 1.0, 1.0)],

        'blue':  [(0.0, 0.2, 0.2),
                (0.3, 0.5, 0.5),
                (0.5, 0.0, 0.0),
                (0.75, 0.0, 0.0),
                (1.0, 1.0, 1.0)]
    }

    audacity_cmap = mcolors.LinearSegmentedColormap('AudacityClassic', cdict)

    # Plot with normalization
    norm = mcolors.Normalize(vmin=-range_db, vmax=0.0)

    plt.figure(figsize=(12, 6))
    plt.pcolormesh(times, frequencies_f, Sxx_db_f, shading='gouraud',
                cmap=audacity_cmap, norm=norm)
    plt.ylim(min_f, max_f)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.title('Spectrogram')
    plt.colorbar(label='dB (relative to peak)')
    #save to png
    #plt.yscale('log')  # for log-frequency spectrogram
    plt.savefig("spectrogram.png", dpi=300, bbox_inches='tight')

    print("runner")