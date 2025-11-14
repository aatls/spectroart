from scipy.signal import ShortTimeFFT
from PIL import Image
import numpy as np

class ImageProcessor:
    """Class that handles image manipulation
    
    ### Attributes
    - pixel_data : 2d list of floats
    - width : int
    - height : int

    ### Methods
    - load_image(infile)
    - generate_audio(samplerate)
    """

    def __init__(self):
        self.pixel_data = None

        self.width = None
        self.height = None

    def load_image(self, infile):
        """Saves given imagefile to the class variables
        
        ### Parameters
        1. infile : str
        """
        image = Image.open(infile).convert("RGB")
        self.pixel_data = image.load()

        self.width, self.height = image.size

    def generate_audio(self, samplerate, min_f, max_f):
        """Generates audio from the saved image
        
        ### Parameters
        1. samplerate : int
        2. min_f : float
        3. max_f : float
        """

        # Window length is 2 x image height because
        # bin[x] = bin[-x] when x < image height
        win_length = 2 * self.height - 1

        n_positive_bins = self.height

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


        series = np.zeros((n_positive_bins, self.width), dtype=float)

        # Linearly space target frequency bins between min_bin and max_bin
        target_bins = np.linspace(min_bin, max_bin, num=self.height)
        target_bins_int = np.round(target_bins).astype(int) # round to nearest integer

        for y in range(self.height):
            row_values = [] # buffer for brightness values of the image row y
            for x in range(self.width):
                normalized = np.array(self.pixel_data[x, self.height - 1 - y]) / 255
                normalized *= [0.5, 1.0, 0.25]
                avg = np.sum(normalized) / 3
                brightness = avg ** 2
                row_values.append(brightness)
            k = int(target_bins_int[y]) # target frequency bin for the row_values
            series[k, :] = row_values # assign values of row_values to row to target frequency bin k

        SFT = ShortTimeFFT(win=np.hanning(win_length),
                        hop=(self.height),
                        fs=samplerate)

        # Create audio with inverse STFT
        output = SFT.istft(series)

        # Normalize output
        output /= np.max(np.abs(output))

        return output
