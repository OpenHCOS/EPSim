# @file cli.py
# @brief CLI of whole tool
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import cmd
import logging
#extend
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
#Spec: about, user commands, test commands
#How/NeedToKnow:
class Cli(cmd.Cmd):
    """Simple command processor example."""    
    def __init__(self,stdout=None):
        cmd.Cmd.__init__(self)
        self.prompt = 'EPSimCLI> '
        pass
############ cli maintain ####################        
    def do_about(self, line):
        """About this software"""
        print("%s version: v%s" %(LSIM_TITLE,LSIM_VERSION))
    def do_quit(self, line):
        """quit"""
        return True
############ top command ####################                      
    def do_reset(self,line):
        """ reset for next run """  
        gc.GAP.reset()
        print("reseted")
        
    def do_status(self,line):
        """ show current status 
            status {desc_id}
            desc_id: 0-summary info, 1- detail info, 2- dot graph
            ex: status 1
        """
        pars=line.split()
        desc_id = 1
        if len(pars)==1:
            desc_id = int(pars[0])   
        logging.info(gc.VIRUS.desc(desc_id))     
        logging.info(gc.MODEL.desc(desc_id))
        logging.info(gc.HC.desc(desc_id))
        logging.info(gc.GAP.mm.desc(desc_id))                   
    
    def do_output(self,line):
        """ output files for analyze
            output {type_id} 
            type_id: 1-per day summary info
            ex: output 1
        """
        pars=line.split()
        type_id = 1
        if len(pars)==1:
            type_id = int(pars[0]) 
        if type_id==1:
            fp = open("output/day_summary.csv", "w")
            fp.write(gc.GAP.mm.desc(1))
            fp.close()

    def do_regression(self,line):
        """ regression for simulation 
            regression {case} {par1} {par2}
            ex: regression 1 3.0 0.2 20 #case=1, r0=3.0, step =0.2, sim_day=20
        """

        pars=line.split()
        case = 1
        r0 = 3.0
        step = 0.2
        sim_days = 20
        if len(pars)>=1:
            case = int(pars[0])
            r0 = float(pars[1])
            step = float(pars[2])
            sim_days=int(pars[3])
        if case == 1: #r0, step, sim_days
            
            for i in range(10):
                gc.GAP.reset()
                
                gc.VIRUS.vm_r0 = r0 + i*step
                gc.GAP.simrun(sim_days)
        
    def do_test(self,line):
        """ current testing """
        pass

    def do_simrun(self, line):
        """Start simulation
            simrun {count}
            ex: simrun 20
        """
        
        pars=line.split()
        count = 20
        if len(pars)==1:
            count = int(pars[0])
        
        gc.GAP.reset()
        gc.GAP.simrun(count)


    