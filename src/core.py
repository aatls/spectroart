# Application logic

import src.imageprocessor as imgprocessor
import src.helpers as helpers

class Core:
    def __init__(self):
        self.imgprocessor = imgprocessor.ImageProcessor()

    def load_image(self, infile):
        self.imgprocessor.load_image(infile)

    def convert(self, outfile, samplerate, min_f, max_f):
        data = self.imgprocessor.generate_audio(samplerate, min_f, max_f)

        helpers.write_audio(outfile, data, samplerate)
