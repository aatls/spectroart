import soundfile as sf
from PIL import Image

def write_audio(outfile, data, samplerate):
    sf.write(outfile, data, samplerate)
    
def load_image(infile):
    image = Image.open(infile).convert("RGB")
    return image
