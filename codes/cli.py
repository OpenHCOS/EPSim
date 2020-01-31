# @file cli.py
# @brief CLI of whole tool
# README: Command line interface
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import cmd
#extend
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
#Spec: local variable maintain, about, user commands, test commands
#How/NeedToKnow:
class Cli(cmd.Cmd):
    """Simple command processor example."""    
    def __init__(self,stdout=None):
        cmd.Cmd.__init__(self)
        self.prompt = 'EPSimCLI> '
        pass
############ cli maintain ####################        
    def do_set(self,line):
        """set scli variable, can be new or update.
        set var_name var_value
        ex: set a 123"""

        pars=line.split()
        if len(pars)==2:
            var = pars[0]
            value = pars[1]
        else:
            return 
        
        if var in ('dev_console_display','log_level_file','log_level_console'):
            value = int(value)
            
        gc.GAP.user_vars[var] = value
        # dynamic apply
        # these variable need to work out, log_level_file, log_level_console

    def do_show(self,line):
        """show simcli variables, if miss variable name, show all
        show variable_name
        system variables list:
            ;log level definition, DEBUG=10,INFO=20,WARNING=30,ERROR=40,CRITICAL=50
            log_level_console=20     #the console message log level
            log_level_file=40        #file message log level
            ;device console real time display
            dev_console_display=1    #(0) don't display (1) display
        ex: show dev_console_display """
        for var in gc.GAP.user_vars.keys():
            print("%s=%s" % ( var , gc.GAP.user_vars[var]))


    
    def do_about(self, line):
        """About this software"""
        print("%s version: v%s" %(LSIM_TITLE,LSIM_VERSION))
    def do_quit(self, line):
        """quit"""
        return True
############ top command ####################                      
    #def do_test1(self, line):
    #    """current debug command"""
    #    self.cli_ebm.do_init("")
    def do_reset(self,line):
        """ reset for next run """
        
        gc.GAP.reset()
        print("reseted")
        
    def do_status(self,line):
        """ show current status 
            status {desc_id}
            ex: status 1
        """
        pars=line.split()
        desc_id = 1
        if len(pars)==1:
            desc_id = int(pars[0])        
        print(gc.MODEL.desc(desc_id))
        print(gc.GAP.mm.desc(desc_id))                   

    def do_regression(self,line):
        """ regression for simulation 
            regression {case} {par1} {par2}
            ex: regression 1 1.5 0.2 10 #case=1, r0=1.5, step =0.2, sim_day=10
        """

        pars=line.split()
        case = 1
        r0 = 1.5
        step = 0.2
        sim_days = 10
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
        
    def do_simrun(self, line):
        """Start simulation
            simrun {count}
            ex: simrun 50
        """
        
        pars=line.split()
        count = 50
        if len(pars)==1:
            count = int(pars[0])
        
        gc.GAP.reset()
        gc.GAP.simrun(count)


    