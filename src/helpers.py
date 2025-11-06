import soundfile as sf

def write_audio(outfile, data, samplerate):
    sf.write(outfile, data, samplerate)
    