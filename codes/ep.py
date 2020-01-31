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
        self.parent = 0 # 被誰感染 seq
        self.childs = [] # 感染了誰 seq
    def add_sick_day(self, sickday_value): # 加一天隨機病程
        self.sick_day += sickday_value
    def random_init(self):
        self.sick_status = SICKSTATUS_INIT # 有症狀...    

        self.sick_day= random.uniform(1,20)
        if self.sick_day >= 20.0:
            self.sick_status = SICKSTATUS_DIE
        elif self.sick_day >= 7.0:
            self.sick_status = SICKSTATUS_SHOW    

#Spec: Manager all patient information
#How/NeedToKnow:        
class PatientMgr():
    def __init__(self):
        self.reset()
    def reset(self):
        self.p_seq=0 # human sequence
        self.patients = {} #patients dict, index by seq
        self.sr_cur = [0,0,0,0,0,0,0,0]
        self.sr_last = []  
        self.root = [] # 外部/感染源傳來， seq  
    def start_init(self):
        patient_start = int(gc.SETTING["PATIENT_START_COUNT"]) 
        #patient_start = 643
        for i in range(patient_start):
            new_patient_id = self.add_patient(0,0,True)
            self.root.append(new_patient_id)
            
    def update_sr(self, sr): # update state record
        self.sr_last = self.sr_cur
        self.sr_cur = sr
        p_new = self.sr_cur[SR_C5] - self.sr_last[SR_C5]
        for i in range(p_new):
            new_patient_id = self.add_patient(0,0) #FIXME
            self.root.append(new_patient_id)
    def add_patient(self,parent,current_day, need_random=False):
        new_patient_id = self.p_seq
        p = Patient(new_patient_id)
        p.sick_start = current_day
        if need_random:
            p.random_init()
        p.parent = parent
        
        self.patients[new_patient_id] = p
        if parent != 0:
            self.patients[parent].childs.append(new_patient_id)
        self.p_seq+=1
        return new_patient_id
    def rpt_status(self):
        return len(self.patients)
    def desc(self,desc_id=0):
        txt_desc=""
        if desc_id==0: # patients count
            txt_desc = "Patients count: %i" %(len(self.patients))
        if desc_id==1: # detail   
            for k in self.patients:
                p = self.patients[k]
                txt_desc += "seq=%i,p_seq=%i-%f\t" % (p.p_seq,p.parent, p.sick_day)
        if desc_id==2: # dot graph
            txt_desc="digraph G {\n"
            for k in self.patients:
                p = self.patients[k]
                txt_desc += "\t%s->%s\n" % (p.parent,p.p_seq)
            txt_desc+="}"            
        return txt_desc
        

#Spec: 
#How/NeedToKnow:       
class StateRecordSets():
    def __init__(self):
        self.srs ={} # key= offset day, number=8 , [offset date, 通報數,疑似數,初驗陰性,排除數,確診數,痊癒數,死亡數] , -1 為 unknow
        
        self.srs[0]=[23,134,106,21,27,1,0,0]
        #self.srs[10]=[24,168, 123 , 23 , 42 , 3 , 0 , 0 ]
        #self.srs[20]=[25,283,156,53,124,3,0,0]
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
        pass
        


#Spec: Support System
#How/NeedToKnow: 
class SupportSys(): 
    def __init__(self): 
        pass

#Spec: Virus model
#How/NeedToKnow: 
class VirusModel(): 
    def __init__(self): 
        self.reset()
        self.pars = []
    def reset(self): # reset for reload setting from file
        random.seed()
        self.vm_mode = int(gc.SETTING["VM_MODE"])
        self.sickday_rnd = float(gc.SETTING["SICKDAY_PERCENT"])
        self.vm_r0 = float(gc.SETTING["VM_R0"]) 
        self.vm_infect_daystart = float(gc.SETTING["VM_INFECT_DAYSTART"]) 
         
        
        
    def age_oneday(self, patient):
        if self.vm_mode == 1:
            patient.sick_day +=  random.uniform(1.0-self.sickday_rnd,1.0+self.sickday_rnd)
            if patient.sick_day >= 20.0:
                patient.sick_status = SICKSTATUS_DIE
            elif patient.sick_day >= 7.0:
                patient.sick_status = SICKSTATUS_SHOW
        else:
            pass

    def infect_byday(self,patient):
        if self.vm_mode == 1:
            if patient.sick_status == SICKSTATUS_DIE or patient.sick_status ==SICKSTATUS_PASS:
                return 0
            if patient.sick_day>= self.vm_infect_daystart and patient.sick_day<=8:
                return self.vm_r0/(8-self.vm_infect_daystart)
            else:
                return 0
        else:
            return 0        