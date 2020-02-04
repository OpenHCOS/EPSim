# @file sim.py
# @brief statup and AP mode selection
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import getopt
import sys
import unittest

#extend
from configobj import ConfigObj
import simpy

#library
import lib.globalclasses as gc
from lib.const import *
import codes.app as app
import codes.model as md
import codes.cli as cli
import codes.ut as ut
import codes.ui as ui

#Spec: program init, mode selection, start
#How/NeedToKnow:
if __name__ =='__main__':
    # Read system parameters which are assigned while we launching "start.py".
    # If the input parameter is invalid, then display usage and return "command
    # line syntax" error code.
    apmode = AP_MODE_NORMAL

    #command line paramters handler
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht", [])
        for opt, arg in opts:
            if opt == '-h':
                print ('sim.py [ -h ] [ -t ]')
                print ('    -h, --help: help message')
                print ('    -t, --test: unit test mode')
                sys.exit()
            elif opt in ("-t", "--test"):
                apmode = AP_MODE_UNITTEST
                print("Running as unittest mode!")
    except getopt.GetoptError:
        print ('usage: sim.py [ -h ] [ -t ]')       
        sys.exit(2) 
    
    

    #init global classes   
    gc.SETTING  = ConfigObj("include/sim.ini") 
    gc.UI = ui.UserInterface()
    gc.VIRUS = md.VirusModel()
    gc.GAP = app.SApp()
    gc.CLI = cli.Cli()
    
    
    #run by different mode
    if apmode == AP_MODE_UNITTEST:
        suite = unittest.TestLoader().loadTestsFromTestCase(ut.UTGeneral)
        unittest.TextTestRunner(verbosity = 2).run(suite)
    else:
        
        gc.CLI.cmdloop()
    
