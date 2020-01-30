# @file model.py
# @brief model used for simulation
# README: model used for simulation
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import logging
import random
from datetime import datetime,timedelta
from codes.ep import *
#extend
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
   
#Spec: Monitor the model, collect the history
#How/NeedToKnow:
class ModelMonitor():
    def __init__(self):
        self.history=[]
        pass

#Spec: Core simulation model
#How/NeedToKnow:
class Model():
    def __init__(self,env):
        #private
        #global: these variables allow to direct access from outside.
        self.env = env
        self.desc_list=[] # some description about the model
                
        fmt = '%Y-%m-%d %H:%M:%S'
        self.dt_start = datetime.strptime(gc.SETTING["MODEL_START_TIME"], fmt)
        self.dt_end = self.dt_start #init value
        
        
        self.patient_mgr = PatientMgr() 
        self.srs= StateRecordSets()
        sr = self.srs.find_byoffset(0) 
        self.patient_mgr.update_sr(sr)
        
        self.model_desc = ""
        
        
    def init(self):
        pass
    def model_setup(self):
        self.env.process(self.patients_run()) 
        self.desc_list.append("model_setup!")
    
    def patients_run(self):
        while True:
            die_list = []
            
            for k in list(self.patient_mgr.patients):
                p = self.patient_mgr.patients[k]
                gc.VIRUS.age_oneday(p)
                if p.sick_status == SICKSTATUS_DIE:
                    die_list.append(k)
            
                inf_rate = gc.VIRUS.infect_ability(p) * gc.HC.infect_capacity(p)
                if random.uniform(0,1) < inf_rate:
                    self.patient_mgr.add_patient()
            for d in die_list:
                del self.patient_mgr.patients[d]
                #self.patient_mgr.add_sr5()
            #logging.info("patients count %i" %(len(self.patient_mgr.patients)))
            yield self.env.timeout(1)  
        
    def get_desc_str(self):
        return "\n".join(self.desc_list)   
    def desc(self):
        return self.patient_mgr.desc()
