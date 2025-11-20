from scipy.signal import ShortTimeFFT
from PIL import Image
import numpy as np
    
def flip_image(image, xy):
    """Flips the image horizontally (x) or vertically (y) and returns flipped image.
    
    
    ### Parameters
    1. xy : str        
    """
    
    # Determine flip direction and do it
    if xy.lower() == "x":
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif xy.lower() == "y":
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("xy must be 'x' for horizontal or 'y' for vertical flip")
    
    return image

def generate_audio(pixel_data, samplerate, min_f, max_f):
    """Generates audio from the saved image
    
    ### Parameters
    1. pixel_data : 2d array
    2. samplerate : int
    3. min_f : float
    4. max_f : float
    """

    pixel_data = np.array(pixel_data)

    width, height = np.shape(pixel_data)[:2]

    # Window length is 2 x image height because
    # bin[x] = bin[-x] when x < image height
    win_length = 2 * height - 1

    n_positive_bins = height

    # Map corresponding FFT bins for min_f and max_f
    min_bin = int(round(min_f * win_length / samplerate))
    max_bin = int(round(max_f * win_length / samplerate))

    # Clip values within the set range
    min_bin = np.clip(min_bin, 0, n_positive_bins - 1)
    max_bin = np.clip(max_bin, 0, n_positive_bins - 1)


    # Ensure all frequencies don't collapse into a single bin.

    if min_bin == max_bin:
        if max_bin < n_positive_bins - 1:
            max_bin = min(min_bin + 1, n_positive_bins - 1)
        else:
            if min_bin > 0:
                min_bin = max(min_bin - 1, 0)


    series = np.zeros((n_positive_bins, width), dtype=float)

    # Linearly space target frequency bins between min_bin and max_bin
    target_bins = np.linspace(min_bin, max_bin, num=height)
    target_bins_int = np.round(target_bins).astype(int) # round to nearest integer

    for y in range(height):
        row_values = [] # buffer for brightness values of the image row y
        for x in range(width):
            normalized = pixel_data[x, height - 1 - y] / 255
            normalized *= [0.2126, 0.7152, 0.0722]
            total = np.sum(normalized)
            brightness = total ** 2
            row_values.append(brightness)
        k = int(target_bins_int[y]) # target frequency bin for the row_values
        series[k, :] = row_values # assign values of row_values to row to target frequency bin k

    SFT = ShortTimeFFT(win=np.hanning(win_length),
                    hop=(height),
                    fs=samplerate)

    # Create audio with inverse STFT
    output = SFT.istft(series)

    # Normalize output
    output /= np.max(np.abs(output))

    return output
