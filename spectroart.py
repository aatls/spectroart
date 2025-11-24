import sys

import src.textui as txtui
import tests.test as test

import src.visualui as visualui

if __name__ == "__main__":


    # Check if program is run with test flag
    if "-t" in sys.argv:
        ui = txtui.TextUi()
        test.run_tests(ui, sys.argv)
    else:        
        visualui.VisualUi()
        raise SystemExit
