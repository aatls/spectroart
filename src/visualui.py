import src.imageprocessor as imageprocessor
import src.helpers as helpers

import tkinter as tk
from tkinter import filedialog

from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

import random
import sounddevice
import shutil



class VisualUi:
    def __init__(self):
        # Input parameters should be saved here
        self.outfile = None
        self.samplerate = 44100 # Default
        self.min_f = 5000
        self.max_f = 21000
        self.audio_duration = 20
        self.scale = "lin" # 'lin' or 'log'

        # Data storage
        self.original_image = None
        self.modified_image = None
        self.generated_audio = None


        # Root window
        self.root = TkinterDnD.Tk()
        self.root.title("Spectroart :D")
        self.root.minsize(900, 500)

        # Holders
        self.left_holder = tk.Frame(self.root, borderwidth=2, relief="groove", padx=10, pady=10)
        self.right_holder = tk.Frame(self.root, borderwidth=2, relief="groove", padx=10, pady=10)

        self.left_holder.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.right_holder.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Panels
        self.input_img_panel = tk.Frame(self.left_holder, borderwidth=2, relief="groove", padx=10, pady=10)
        self.output_aud_panel = tk.Frame(self.left_holder, borderwidth=2, relief="groove", padx=10, pady=10)
        self.output_img_panel = tk.Frame(self.right_holder, borderwidth=2, relief="groove", padx=10, pady=10)

        # Grid expansion
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # ------------------ Input Image Panel ------------------
        tk.Label(self.input_img_panel, text="Image path").pack(pady=5)

        self.image_path = tk.StringVar()
        
        entry = tk.Entry(self.input_img_panel, textvariable=self.image_path, width=50)
        entry.drop_target_register(DND_FILES)
        entry.dnd_bind("<<Drop>>", lambda e: self.image_path.set(e.data))
        entry.pack(padx=10, pady=10)

        # ------------------ Output Audio Panel ------------------
        tk.Label(self.output_aud_panel, text="Generated audio").pack(pady=5)

        self.audio_play_button = tk.Button(self.output_aud_panel, text="Play Audio", command=self.on_play)
        self.audio_stop_button = tk.Button(self.output_aud_panel, text="Stop Audio", command=self.on_stop)
        self.audio_download_button = tk.Button(self.output_aud_panel, text="Download Audio", command=self.on_download)

        self.audio_play_button.pack(pady=5)
        self.audio_stop_button.pack(pady=5)
        self.audio_download_button.pack(pady=5)

        # ------------------ Output Image Panel ------------------
        tk.Label(self.output_img_panel, text="Spectrogram").pack(pady=5)

        rect = tk.Frame(self.output_img_panel, width=400, height=300, bg="lightblue")
        rect.pack(padx=20, pady=20)


        pil_img = Image.open("./tests/wayne.jpg")
        pil_img = pil_img.resize((400, 300))
        
        img = ImageTk.PhotoImage(pil_img)
        

        self.img_label = tk.Label(rect, image=img)
        self.img_label.pack(expand=True)


        # ------------------ Spectrogram Settings ------------------
        self.spectro_settings = tk.Frame(self.left_holder, borderwidth=0, relief="groove")
        # self.spectro_settings.pack()

        self.ref_img_button = tk.Button(self.right_holder, text="Generate spectrogram", command=self.on_generate)
        self.ref_img_button.pack(pady=10)

        tk.Label(self.spectro_settings, text="Flip axis: ").pack(side = "left")

        # Variables
        self.flip_x = tk.IntVar()
        self.flip_y = tk.IntVar()
        self.toggle_r = tk.IntVar(value=1)
        self.toggle_g = tk.IntVar(value=1)
        self.toggle_b = tk.IntVar(value=1)

        # Checkboxes
        chk1 = tk.Checkbutton(self.spectro_settings, text="X", variable=self.flip_x)
        chk2 = tk.Checkbutton(self.spectro_settings, text="Y", variable=self.flip_y)

        for chk in [chk1, chk2]:
            chk.pack(side="left", pady=5)

        tk.Label(self.spectro_settings, text="Scale: ").pack(side = "left")

        options = ["Linear", "Logarithmic"]
        self.selected_scale = tk.StringVar(value=options[0]) 

        dropdown = tk.OptionMenu(self.spectro_settings, self.selected_scale, *options, command=self.on_scale_change)
        dropdown.pack(side="right", pady=10)


        # Convert button
        convert_button = tk.Button(self.left_holder, text="Convert To Audio", command=self.on_convert)

        # Pack inside holders
        self.input_img_panel.pack(padx=10, pady=10, fill="both")
        self.spectro_settings.pack()
        convert_button.pack(pady=10)
        self.output_aud_panel.pack(padx=10, pady=10, fill="both")
        self.output_img_panel.pack(padx=10, pady=10, expand=True, fill="both")

        print(self.output_aud_panel.cget("bg"))
        self.set_output_state(False)
        

        # Start main loop
        self.root.mainloop()

    # ------------------ Methods ------------------
    def on_generate(self):
        if self.image_path.get():
            print(f"x={self.flip_x.get()}, y={self.flip_y.get()}")

            self.image = self.image_path.get().replace("{", "").replace("}", "")
            self.set_image(self.image)
            self.generate_spectrogram()
            
        else:
            print("No file selected")

            # Random img test
            img = random.choice(["tests\loveless.png", "tests\wayne.jpg"])
            self.set_image(img)

    def on_convert(self):
        
        if self.image_path.get():
            print("Converting...", end="\t")
            self.set_output_state(True)
            self.convert()
            print("Converted!")
        else:
            print("No file selected")

    def convert(self):

        self.image = self.image_path.get().replace("{", "").replace("}", "")
        
        

        # load image
        self.original_image = helpers.load_image(self.image)
        self.modified_image = self.original_image 

        flip_x, flip_y = self.flip_x.get(), self.flip_y.get()
        if flip_x:
            self.modified_image = imageprocessor.flip_image(self.modified_image, "x")
        if flip_y:
            self.modified_image = imageprocessor.flip_image(self.modified_image, "y")

        # self.set_image(self.image)
        self.set_pil_image(self.modified_image)
        
        # converts {/path/to/image.ext} to tests/image.wav
        self.outfile = self.image_path.get().split('/')[-1]
        self.outfile = "tests\\" + self.outfile.split('.')[0] + ".wav"

        audio = imageprocessor.generate_audio(self.modified_image, self.samplerate, self.min_f, self.max_f, self.audio_duration, self.scale)
        print(self.scale)

        self.generated_audio = audio

    def on_play(self):
        if self.generated_audio.any():
            print("Playing...")
            sounddevice.play(self.generated_audio, self.samplerate)
        else: 
            print("No audio to play")

    def on_stop(self):
        print("Stopped audio...")
        sounddevice.stop()

    def on_download(self):
        print("Downloading...")
        if self.generated_audio.any():
            save_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                initialfile=self.outfile.split('\\')[-1],
                filetypes=[("Audio files", "*.wav"), ("All files", "*.*")]
            )
            if save_path: 
                print("selected: ", save_path)
                helpers.write_audio(save_path, self.generated_audio, self.samplerate)
        else: 
            print("No audio to download")



    def set_image(self, path):
        pil_img = Image.open(path)
        pil_img = pil_img.resize((400, 300))  # resize always 
        new_img = ImageTk.PhotoImage(pil_img)

        self.img_label.config(image=new_img)
        self.img_label.image = new_img

    def set_pil_image(self, image):
        image = image.resize((400, 300))  # resize always 
        new_img = ImageTk.PhotoImage(image)

        self.img_label.config(image=new_img)
        self.img_label.image = new_img


    def set_output_state(self, toggle):
        for button in [self.audio_play_button, self.audio_stop_button, self.audio_download_button, self.ref_img_button]:
            if toggle:
                button.configure(bg="gray90")
                button.configure(state="normal")
            else:
                button.configure(bg="light gray")
                button.configure(state="disabled")

    def generate_spectrogram(self):
        print("is it running?")
        helpers.spectrogramify(self.generated_audio, self.samplerate, self.min_f, self.max_f, self.scale)
        print("We have runned")
        self.set_image("spectrogram.png")

    def on_scale_change(self, value):
        self.scale = value[:3].lower()
        print("Scale set to ", self.scale) 