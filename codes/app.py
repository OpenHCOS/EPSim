# @file app.py
# @brief The main module to maintain whole app
# README: Application wide management unit
# MODULE_ARCH:  ExecuteCmd, globalclasses_init, globallist_init
# CLASS_ARCH: SimApp
# GLOBAL USAGE: execmd_par

#standard
import logging
from datetime import datetime,timedelta

#extend
import simpy
import matplotlib.dates as mdate
#library
import codes.model as md
import codes.ui as ui
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
#Spec: simulation control, log managment, setting load/save
#How/NeedToKnow:
class SApp:
    def __init__(self):
        self.init_log()
        logging.info("%s version: v%s" %(LSIM_TITLE,LSIM_VERSION))
        self.reset()
        
        
    def init_log(self):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='output/sim.log',
                            filemode='a')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO) #logging.INFO
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        
        # Now, we can log to the root logger, or any other logger. First the root...
        #logging.info('Logger initialed')
    
    def load_setting(self):
        pass
    def save_setting(self):
        pass
    def reset(self):
        gc.VIRUS.reset()
        gc.MODEL = md.Model(simpy.Environment())
        self.user_vars={}
        self.mm = md.ModelMonitor()
         
    def simrun(self, v_until):
        """current debug command"""
        #self.reset()
        
        gc.MODEL.model_setup()
        
        
        logging.info("Simulation start!\nSimulation Descriptor:\n%s" %(gc.MODEL.get_desc_str() ) )
        
        for i in range(1,v_until):
            gc.MODEL.model_day = i
            gc.MODEL.env.run(until=i)
            gc.MODEL.dt_end = gc.MODEL.dt_start + timedelta(days=i)
            
            self.mm.history_x.append(gc.MODEL.dt_end)
            self.mm.history.append(gc.MODEL.patient_mgr.rpt_status())
            #logging.info(gc.MODEL.desc() )
        print("total history: %s" % (self.mm.history))
        gc.MODEL.model_desc = "model=%i,sickday_rnd=%.2f,vm_r0=%.2f" % (gc.VIRUS.vm_mode,gc.VIRUS.sickday_rnd,gc.VIRUS.vm_r0)
        gc.UI.test(self.mm.history_x, self.mm.history,gc.MODEL.model_desc)
    
