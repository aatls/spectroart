def run_tests(ui, argv):
    if argv[-1] != "-t":
        infiles = argv[argv.index("-t") + 1, :]
    else:
        infiles = ["./tests/wayne.jpg", "./tests/loveless.png"]

    for infile in infiles:

        print("\nTest infile: " + infile + "\n")

        print("Testing 'load'..\n")

        ui.infile = infile
        ui.load_image()

        print("\nTesting 'flip'..\n")

        ui.flip_image("X")
        ui.flip_image("X")
        ui.flip_image("Y")
        ui.flip_image("Y")

        print("\nTesting 'convert'..\n")

        ui.outfile = '.' + infile.split('.')[-2] + "-test-result.wav"
        ui.convert()

    print("\nTesting 'exit'..\n")

    ui.exit_program()
