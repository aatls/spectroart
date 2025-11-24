import sys

import src.textui as txtui
import tests.test as test

import src.visualui as visualui

if __name__ == "__main__":



    if True:
        visualui.VisualUi()
        raise SystemExit
    
    ui = txtui.TextUi()


    # Check if program is run with test flag
    if "-t" in sys.argv:
        test.run_tests(ui, sys.argv) # Run tests
    else:        
        ui.start() # Starts the program

    
