import soundfile as sf
from PIL import Image
import numpy as np

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
