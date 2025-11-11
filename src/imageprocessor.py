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
        image = Image.open(infile)
        self.pixel_data = image.load()

        self.width, self.height = image.size

    def generate_audio(self, samplerate):
        """Generates audio from the saved image
        
        ### Parameters
        1. samplerate : int
        """

        # Window length is 2 x image height because
        # bin[x] = bin[-x] when x < image height
        win_length = 2 * self.height - 1

        # STFT series is generated here
        series = [[] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                normalized = np.array(self.pixel_data[x, self.height - 1 - y]) / 255 # Normalize pixel values to range 0.0 - 1.0
                # normalized *= [0.5, 1, 0.25]                        # Apply weights to rgb values
                avg = np.sum(normalized) / 3
                brightness = avg**2                                 # Easy way to add contrast to brightness values
                series[y].append(brightness)

        series = np.array(series)

        SFT = ShortTimeFFT(win=np.hanning(win_length),
                        hop=(self.height),
                        fs=samplerate)

        # Create audio with inverse STFT
        output = SFT.istft(series)

        # Normalize output
        output /= np.max(np.abs(output))

        return output
