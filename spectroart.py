import sys

import src.textui as txtui
import tests.test as test

if __name__ == "__main__":

    ui = txtui.TextUi()

    # Check if program is run with test flag
    if "-t" in sys.argv:
        # Run tests
        test.run_tests(ui)
    else:        
        # Starts the program
        ui.start()
