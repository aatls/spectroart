# Application logic

import src.imageprocessor as imgprocessor
import src.helpers as helpers

class Core:
    def __init__(self):
        self.imgprocessor = imgprocessor.ImageProcessor()

    def load_image(self, infile):
        self.imgprocessor.load_image(infile)

    def convert(self, outfile):
        data, fs = self.imgprocessor.generate_audio()

        helpers.write_audio(outfile, data, fs)
