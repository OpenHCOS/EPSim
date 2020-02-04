# @file ut.py
# @brief The main unit test program of whole project
#    refer UTGeneral functions
#    print the suggested procedure in the console
#    print the suggested check procedure in the console
#    support current supported important features
#    this unit test include in the release procedure
# MODULE_ARCH:  
# CLASS_ARCH: UTGeneral
# GLOBAL USAGE: 

#standard
import unittest
#homemake
import lib.globalclasses as gc
from lib.const import *



##### Unit test section ####
#the test ID provide the order of testes. 
#Spec: 
#How/NeedToKnow:  
class UTGeneral(unittest.TestCase):
    #local
    #ID:0-99
    def test_001_setting_signature(self):
        print("\nCheck signature and to see program started")
        self.assertEqual(gc.SETTING["SIGNATURE"],'EPSim')        

    def test_002_cli_help(self):
        gc.CLI.do_help("")
        self.assertEqual(True,True)        

    def test_003_simrun(self):
        gc.CLI.do_simrun("20")
        self.assertEqual(True,True)

    def test_004_status(self):
        gc.CLI.do_status("1")
        gc.CLI.do_status("2")
        self.assertEqual(True,True)

    def test_005_output(self):
        gc.CLI.do_output("1")
        self.assertEqual(True,True)

    def test_006_regression(self):
        gc.CLI.do_regression("1 3.0 0.1 10")
        self.assertEqual(True,True)
        
        
        