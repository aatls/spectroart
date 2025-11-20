import src.imageprocessor as imageprocessor
import src.helpers as helpers

class TextUi:
    def __init__(self):
       # Input parameters should be saved here
        self.infile = None
        self.outfile = None
        self.samplerate = 44100 # Default
        self.min_f = 2000
        self.max_f = 10000

        # Data storage
        self.original_image = None
        self.modified_image = None
        self.generated_audio = None

    def start(self):
        greetings = """
Hello! 
Welcome to Spectroart, a nice program to make spectrogram art.
Write 'help' if you want some help."""

        print(greetings)

        # Start UI loop
        while True:
            print()
            cmd = input("Gimme instructions: ")
            print()

            match cmd:
                case "help":
                    self.print_help()
                
                case "load":
                    self.infile = input("    Path to image: ")
                    self.load_image()

                case "convert":
                    self.outfile = input("    Outfile name (Leave blank for [infile].wav): ")
                    self.convert()

                case "exit":
                    self.exit_program()

                case "test":
                    self.infile = ".\wayne.jpg"
                    self.load_image()
                    self.outfile = "test.wav"
                    self.convert()
                    
                case "flip":
                    xy = input("    Type X to flip horizontally Y to flip vertically: ")
                    self.flip_image(xy)
                case _:
                    print(f"    '{cmd}' is not a valid command. Type 'help' for list of the commands")


    def print_help(self):
        help_msg = """    Instructions:

    load:       Loads an image file.
                Enter the full path to the image.
                Working image formats not yet specified.
            
    convert:    Converts the image to audio.
                Saves the result to user specified file or
                [infile].wav if outfile left blank
                
    test:       Runs the program with default testing
                parameters.    
                
    flip:       Flips image horizontally or vertically.        
                
    exit:       Exit the program."""

        print(help_msg)

    def load_image(self):
        self.original_image = helpers.load_image(self.infile)
        self.modified_image = self.original_image

        print("    Success")
        
    def flip_image(self, xy):
        self.modified_image = imageprocessor.flip_image(self.modified_image, xy)

        print("Flipped")

    def convert(self):
        if self.outfile == "":
            # converts /path/to/infile.ext to ./infile.wav
            self.outfile = self.infile.split('/')[-1]
            self.outfile = self.outfile.split('.')[0] + ".wav"

        audio = imageprocessor.generate_audio(self.modified_image, self.samplerate, self.min_f, self.max_f)

        helpers.write_audio(self.outfile, audio, self.samplerate)

        print(    f"Output written to {self.outfile}")

    def exit_program(self):
        print("    See you later!")
        exit()
