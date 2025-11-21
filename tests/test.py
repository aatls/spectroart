import platform

def run_tests(ui):
    path_to_img = None

    if platform.system() == "Windows":
        path_to_img = ".\wayne.jpg"
    else:
        path_to_img = "./wayne.jpg"

    print("Testing 'load'..\n")

    ui.infile = path_to_img
    ui.load_image()

    print("\nTesting 'flip'..\n")

    ui.flip_image("X")
    ui.flip_image("X")
    ui.flip_image("Y")
    ui.flip_image("Y")

    print("\nTesting 'convert'..\n")

    ui.outfile = "test-result.wav"
    ui.convert()

    print("\nTesting 'exit'..\n")

    ui.exit_program()
