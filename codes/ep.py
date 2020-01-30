# @file ep.py
# @brief  application core logic
# README:
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import random
#extend
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
#Spec: 
#How/NeedToKnow:
class Human():
    def __init__(self,p_seq):
        self.p_seq = p_seq
        self.location_id = 0


#Spec: 
#How/NeedToKnow:
class Patient(Human):
    def __init__(self,p_seq):
        Human.__init__(self,p_seq)
        self.sick_start  = 0 # 被感染日
        self.sick_day=0
        self.sick_status = 0 # 有症狀...
        self.attrs = [] # 各種屬性
    def add_sick_day(self, sickday_value): # 加一天隨機病程
        self.sick_day += sickday_value

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
            self.add_patient()
    def add_patient(self):
        p = Patient(self.p_seq)
        self.patients[self.p_seq] = p
        self.p_seq+=1
    def rpt_status(self):
        return len(self.patients)
    def desc(self,desc_id=0):
        txt_desc=""
        if desc_id==0:
            txt_desc = "Patients count: %i" %(len(self.patients))
            
        else:
            for k in self.patients:
                p = self.patients[k]
                txt_desc += "%i-%f\t" % (p.p_seq, p.sick_day)
        return txt_desc
        

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

#Spec: Health Care System
#How/NeedToKnow: 
class HCSys(): 
    def __init__(self): 
        self.reset()
    def reset(self): # reset for reload setting from file
        self.hc_infect_capacity = float(gc.SETTING["HC_INFECT_CAPACITY"])    
    def infect_capacity(self,patient):
        return self.hc_infect_capacity  

#Spec: Support System
#How/NeedToKnow: 
class SupportSys(): 
    def __init__(self): 
        pass

#Spec: Virus model
#How/NeedToKnow: 
class VirusModel(): 
    def __init__(self): 
        self.R0 = 1
        self.reset()
        self.pars = []
    def reset(self): # reset for reload setting from file
        random.seed()
        self.vm_mode = int(gc.SETTING["VM_MODE"])
        self.sickday_rnd = float(gc.SETTING["SICKDAY_PERCENT"])
        
        
    def age_oneday(self, patient):
        if self.vm_mode == 1:
            patient.sick_day +=  random.uniform(1.0-self.sickday_rnd,1.0+self.sickday_rnd)
            if patient.sick_day >= 20.0:
                patient.sick_status = SICKSTATUS_DIE
            elif patient.sick_day >= 7.0:
                patient.sick_status = SICKSTATUS_SHOW
        else:
            pass
    def infect_ability(self,patient):
        if self.vm_mode == 1:
            if patient.sick_day>= 3.0:
                return 1.0
            else:
                return 0
        else:
            return 0
