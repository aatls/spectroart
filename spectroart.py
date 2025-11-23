import sys

import src.textui as txtui
import tests.test as test

if __name__ == "__main__":

    ui = txtui.TextUi()

    # Check if program is run with test flag
    if "-t" in sys.argv:
        test.run_tests(ui, sys.argv) # Run tests
    else:        
        ui.start() # Starts the program
