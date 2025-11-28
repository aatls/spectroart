from scipy.signal import ShortTimeFFT
from PIL import Image
import numpy as np

import src.helpers as helpers
    
def flip_image(image, xy):
    """Flips the image horizontally (x) or vertically (y) and returns flipped image.
    
    
    ### Parameters
    1. image : PIL Image object
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

def generate_audio(image, samplerate, min_f, max_f, duration=1):
    """Generates audio from the input image
    
    ### Parameters
    1. pixel_data : PIL Image object
    2. samplerate : int
    3. min_f : float
        - Audio minimum frequency (Hz)
    4. max_f : float
        - Audio maximum frequency (Hz)
    5. duration : float
        - Audio duration in seconds
    """

    # Helper functions to make code more readable
    def bw_conversion(pixel_data, weights=[1,1,1]):
        # Apply weights to RGB values
        pixel_data *= weights
        # Pixel brightness = the mean of the RGB values
        pixel_data = pixel_data.mean(axis=2)

        return pixel_data

    def normalize(data, old_range, new_range):
        data *= new_range / old_range

        return data

    def add_power_contrast(data, power):
        data **= power

        return data

    def generate_short_time_fourier_series(image, win_length, min_f, max_f):
        height, width = np.shape(image)[:2]

        n_bins = height

        # Map corresponding FFT bins for min_f and max_f
        min_bin = int(round(min_f * win_length / samplerate))
        max_bin = int(round(max_f * win_length / samplerate))

        # Clip values within the set range
        min_bin = np.clip(min_bin, 0, n_bins - 1)
        max_bin = np.clip(max_bin, 0, n_bins - 1)

        # Ensure all frequencies don't collapse into a single bin.
        if min_bin == max_bin:
            if max_bin < n_bins - 1:
                max_bin = min(min_bin + 1, n_bins - 1)
            else:
                if min_bin > 0:
                    min_bin = max(min_bin - 1, 0)

        series = np.zeros((n_bins, width), dtype=float)

        # Linearly space target frequency bins between min_bin and max_bin
        target_bins = np.logspace(np.log10(min_bin), np.log10(max_bin), num=height)
        target_bins_int = np.round(target_bins).astype(int) # round to nearest integer

        for y in range(height):
            k = int(target_bins_int[y]) # target frequency bin for the row_values
            series[k, :] = image[height - y - 1, :] # assign values of row_values to row to target frequency bin k

        return series

    def set_audio_duration(image, duration, samplerate, win_length, overlap=0.5):
        sample_target_amount = duration * samplerate

        image_height = np.shape(image)[0]
        new_image_width = int(np.ceil(sample_target_amount / (win_length * overlap)))

        output = np.empty((image_height, new_image_width))

        for i in range(image_height):
            output[i, :] = helpers.resize_array(image[i, :], new_image_width)

        return output

    # Convert the pixel data into a numpy array with type 'float'
    # Pixel array is saved in format [y, x]
    image = np.array(image).astype(float)

    # Modify the pixel data
    image = bw_conversion(image, weights=[0.2126, 0.7152, 0.0722])
    image = normalize(image, 255, 1)
    image = add_power_contrast(image, 2.5)

    height, _ = np.shape(image)[:2]

    # Window length is 2 x image height because
    # bin[x] = bin[-x] when x < image height
    win_length = 2 * height - 1

    image = set_audio_duration(image, duration, samplerate, win_length)
    series = generate_short_time_fourier_series(image, win_length, min_f, max_f)

    SFT = ShortTimeFFT(win=np.hanning(win_length),
                    hop=(win_length // 2),
                    fs=samplerate)

    # Create audio with inverse STFT
    output = SFT.istft(series)

    # Normalize output
    output /= np.max(np.abs(output))

    return output
