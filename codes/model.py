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
#extend
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
#Spec: One factory entity
#How/NeedToKnow:
class Human():
    def __init__(self,p_seq):
        self.p_seq = p_seq


#Spec: Manager all patient information
#How/NeedToKnow:        
class PatientMgr():
    def __init__(self):
        self.p_seq=0 # human sequence
        self.patients = {} #patients dict, index by seq
        self.sr_cur = [0,0,0,0,0,0,0,0]
        self.sr_last = []
    def update_sr(self, sr): # update state record
        self.sr_last = self.sr_cur
        self.sr_cur = sr
        p_new = self.sr_cur[SR_C5] - self.sr_last[SR_C5]
        for i in range(p_new):
            human = Human(self.p_seq)
            self.patients[self.p_seq] = human
            self.p_seq+=1
    def add_sr5(self):
        human = Human(self.p_seq)
        self.patients[self.p_seq] = human
        self.p_seq+=1
    def rpt_status(self):
        return len(self.patients)
    def desc(self):
        return "sr_c5 = %i" % (self.p_seq)
        

#Spec: 
#How/NeedToKnow:       
class StateRecordSets():
    def __init__(self):
        self.srs ={} # key= offset day, number=8 , [offset date, 通報數,疑似數,初驗陰性,排除數,確診數,痊癒數,死亡數] , -1 為 unknow
        self.srs[0]=[23,134,106,21,27,1,0,0]
        self.srs[10]=[24,168, 123 , 23 , 42 , 3 , 0 , 0 ]
        self.srs[20]=[25,283,156,53,124,3,0,0]
    def find_byoffset(self,od):
        if od in self.srs:
            return self.srs[od]
        else:
            return None
    
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
        
        
    def init(self):
        pass
    def entity_setup(self):
        self.env.process(self.update_sr_run()) 
        self.env.process(self.infection_run()) 
        self.desc_list.append("entity_setup!")
    def update_sr_run(self):
        yield self.env.timeout(1)  
        pass
    def infection_run(self):
        while True:
            self.patient_mgr.add_sr5()
            yield self.env.timeout(1)  
        
    def get_desc_str(self):
        return "\n".join(self.desc_list)   
    def desc(self):
        return self.patient_mgr.desc()
