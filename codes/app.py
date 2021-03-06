# @file app.py
# @brief The main module to maintain whole app
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
        logging.info("HCOS - %s version: v%s" %(LSIM_TITLE,LSIM_VERSION))
        #logging.info("%s" %(""))
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
        gc.SETTING.reload()
        gc.VIRUS.reset()
        gc.MODEL = md.Model(simpy.Environment())
        gc.MODEL.patient_mgr.start_init()
        gc.MODEL.srs.load_sr()
        gc.HC = md.HCSys()
        self.user_vars={}
        self.mm = md.ModelMgr()
                 
    def simrun(self, v_until):
        """current debug command"""
        #self.reset()
        
        gc.MODEL.model_setup()
                
        for i in range(1,v_until):
            gc.MODEL.model_day = i
            
            logging.info("model_day=%i,dr0=%f" %(i,gc.VIRUS.dr0))
            gc.MODEL.env.run(until=i)
            gc.MODEL.dt_end = gc.MODEL.dt_start + timedelta(days=i)
            logging.info("%s simulated!" %(gc.MODEL.dt_end.strftime('%Y/%m/%d')))
            self.mm.append(gc.MODEL)
            
            #logging.info(gc.MODEL.desc() )
        logging.info("total history: %s" % (self.mm.desc(0)))
        gc.MODEL.model_desc = "rR0=%.2f,DAY_RATE=%.2f,INFECT_DAYS=%.2f" % (gc.VIRUS.vm_r0*gc.VIRUS.dr0,gc.VIRUS.infect_day_rate,gc.VIRUS.infect_days)
        gc.UI.plot(self.mm.history_x, self.mm.pms_info(0),gc.MODEL.model_desc,"%s" %(gc.VIRUS.desc(0)))
        gc.UI.plot(self.mm.history_x, self.mm.pms_info(1),gc.MODEL.model_desc,"%s" %(gc.VIRUS.desc(0)))
    
