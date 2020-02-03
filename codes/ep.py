# @file ep.py
# @brief  application core logic
# README:
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import random
from datetime import datetime
#extend
import csv
import json
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
        self.sick_day=0 #模擬病了幾日
        self.sick_act_day=0 #真實病了幾日
        self.sick_status = 0 # 有症狀...
        self.attrs = [] # 各種屬性
        self.parent = 0 # 被誰感染 seq
        self.childs = [] # 感染了誰 seq
        self.infect_days = 0 # 可感染幾天
        self.infect_count = 0
        self.b_random = False # 是否被隨機產生
    def add_sick_day(self, sickday_value): # 加一天隨機病程
        self.sick_day += sickday_value
    def desc(self,desc_id=0):
        txt_desc = "seq=%i,p_seq=%i,sick_status=%i,infect_days=%i,sick_day=%f,infect_count=%i\n" % (self.p_seq,self.parent,  self.sick_status, self.infect_days,self.sick_day,self.infect_count)
        return txt_desc
        


#Spec: Manager all patient information
#How/NeedToKnow:        
class PatientMgr():
    def __init__(self):
        self.reset()
    def reset(self):
        self.p_seq=0 # human sequence
        self.patients = {} #patients dict, index by seq
        self.dies = {}
        self.p_pass = {}
        self.sr_cur = [0,0,0,0,0,0,0,0]
        self.sr_last = []  
        self.root = [] # 外部/感染源傳來， seq
        self.inf_count = 0  #非初始感染數 
        self.day_usage = None #object
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
        
        gc.VIRUS.patient_init(p,need_random)
        p.parent = parent
        
        self.patients[new_patient_id] = p
        if parent != 0:
            self.patients[parent].childs.append(new_patient_id)
        self.p_seq+=1
        if need_random==False:
            self.inf_count+=1
        return new_patient_id
    def update_day_usage(self):
        self.day_usage = gc.HC.patients_day_usage(self.patients)
    def rpt_status(self):
        # SICKSTATUS_INIT=0, SICKSTATUS_SHOW=1  # 有症狀, SICKSTATUS_HEAVY=2 # 重症
        init_count = 0
        show_count = 0
        heavy_count = 0 
        for k in self.patients:
            p = self.patients[k]
            if p.sick_status == SICKSTATUS_INIT:
                init_count +=1
            elif p.sick_status == SICKSTATUS_SHOW:
                show_count +=1
            elif p.sick_status == SICKSTATUS_HEAVY:
                heavy_count+=1
            else: #pass or die
                pass
                
        return [init_count,show_count,heavy_count]
    def desc(self,desc_id=0):
        txt_desc = "------ PatientMgr Description: ------\n"
        if desc_id==0: # patients count
            txt_desc += "Patients count: %i" %(len(self.patients))
        if desc_id==1: # detail 
            
            txt_desc += "Patients count: %i, Die count=%i, Pass count=%i, infect count=%i\n" %(len(self.patients),len(self.dies),len(self.p_pass),self.inf_count)  
            txt_desc += "Die rate=%f,Pass rate=%f\n" %(float(len(self.dies))/len(self.patients),float(len(self.p_pass))/len(self.patients)) 
            for k in self.patients:
                p = self.patients[k]
                #txt_desc += p.desc(desc_id)
            infect_count = 0    
            p_count = 0
            sick_act_day = 0
            for k in self.dies:
                p = self.dies[k]
                if not p.b_random:
                    infect_count += p.infect_count
                    sick_act_day += p.sick_act_day
                    p_count += 1
            if p_count>0:
                txt_desc += "average infect_count(die)=%f,sick_act_day(die)=%f\t" %(float(infect_count)/p_count,float(sick_act_day)/p_count)
            infect_count = 0
            p_count = 0
            sick_act_day = 0
            for k in self.p_pass:
                p = self.p_pass[k]
                if not p.b_random:
                    infect_count += p.infect_count
                    sick_act_day += p.sick_act_day
                    p_count += 1
            if p_count>0:
                txt_desc += "average infect_count(pass)=%f, sick_act_day(pass)=%f\n" %(float(infect_count)/p_count,float(sick_act_day)/p_count)
            txt_desc += "HCSys day usages=%s\n" % self.day_usage
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
        self.record_file = gc.SETTING["RECORD_FILE"]
        self.sr_x = [] # 比對紀錄 x (日期)
        self.sr_y = [] # 比對紀錄 y (人數)
    def find_byoffset(self,od):
        if od in self.srs:
            return self.srs[od]
        else:
            return None
    def load_sr(self):
        with open('include/' + self.record_file, 'r') as f:
            rows = csv.reader(f)
            self.sr_x = []
            self.sr_y = []

            for raw in rows:
                self.sr_x.append(datetime.strptime(raw[0],"%Y/%m/%d"))
                self.sr_y.append(int(raw[1]))
        

#Spec: Health Care System
#How/NeedToKnow: 
class HCSys(): 
    def __init__(self): 
        self.reset()
    def reset(self): # reset for reload setting from file
        self.usage_file = gc.SETTING["USAGE_FILE"]
        self.usage = {}
        self.load_usage()
        
    def load_usage(self):
        with open('include/' + self.usage_file, 'r') as json_file:
            self.usage = json.load(json_file)
        #print(json.dumps(self.usage))
    def desc(self,desc_id=0):
        txt_desc = "------ HCSys Setting: ------\n"
        return "%s%s\n" % (txt_desc, self.usage)
    def patients_day_usage(self, patients): 
        #'t1_day_usage': [{'病床': 1}, {'護士': 0.2}, {'醫生': 0.05}]
        day_usages = {}
        for pk in patients:
            p = patients[pk]
            if p.sick_status == SICKSTATUS_HEAVY:
                cat= "heavy_day_usage"
            elif p.sick_status == SICKSTATUS_SHOW:
                cat = "show_day_usage"
            else:
                cat = "" 
            if not cat =="":
                for item in self.usage[cat]:  
                    ik = list(item.keys())[0]
                    if not ik in day_usages.keys():
                        day_usages[ik] = 0
                    day_usages[ik] += item[ik]
        return day_usages
        #return "HCSys day usages=%s" %(day_usages)


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

        self.infect_daystart = float(gc.SETTING["INFECT_DAYSTART"]) 
        incubation_period = gc.SETTING["INCUBATION_PERIOD"] # 2,14 #潛伏期
        show_to_end = gc.SETTING["SHOW_TO_END"] #5,14 #有症狀到結束的天數
        pars=incubation_period.split()
        self.incubation_period = [int(pars[0]),int(pars[1])]
        
        pars=show_to_end.split()
        self.show_to_end = [int(pars[0]),int(pars[1])]
        self.infect_days = float(gc.SETTING["INFECT_DAYS"]) #可傳染天數
        
        self.show_to_heavy_rate= float(gc.SETTING["SHOW_TO_HEAVY_RATE"])
        self.infect_day_rate= float(gc.SETTING["INFECT_DAY_RATE"])
        
    # sick_day = 1 +- sickday_rnd
    # 0->1 : 潛伏期內隨機發生
    # 1->2 : show_to_end 內隨機
    # 2->3 : 隨機發生
    # 1->3 : show_to_end 內隨機
    def age_oneday(self, patient):
        if self.vm_mode == 1:
            patient.sick_day +=  random.uniform(1.0-self.sickday_rnd,1.0+self.sickday_rnd)
            patient.sick_act_day +=1
            if patient.sick_status == SICKSTATUS_INIT:
                if patient.sick_day >= self.incubation_period[0]:
                    if random.uniform(0,1) <= 1.0/(self.incubation_period[1]/2):
                        patient.sick_status = SICKSTATUS_SHOW
            elif patient.sick_status == SICKSTATUS_SHOW:
                if random.uniform(0,1) <= 1.0/self.show_to_end[1]:
                    patient.sick_status = SICKSTATUS_HEAVY
                elif random.uniform(0,1) <= 1.0/self.show_to_end[1]:
                    patient.sick_status = SICKSTATUS_PASS
            elif patient.sick_status == SICKSTATUS_HEAVY:
                if random.uniform(0,1) <= 1.0/self.show_to_end[0]:
                    patient.sick_status = SICKSTATUS_SHOW
                elif random.uniform(0,1) <= 1.0/self.show_to_end[0]:
                    patient.sick_status = SICKSTATUS_DIE
            else:
                pass
            
            if patient.sick_day >= self.incubation_period[1] + self.show_to_end[1]:
                patient.sick_status = SICKSTATUS_PASS

    def infect_byday(self,patient):
        if self.vm_mode == 1:
            if patient.sick_status == SICKSTATUS_DIE or patient.sick_status ==SICKSTATUS_PASS:
                return 0
            if patient.sick_day>= self.infect_daystart and patient.sick_day<=(self.infect_days+self.infect_daystart):
                return self.vm_r0/(self.infect_days) * self.infect_day_rate 
            else:
                return 0
        else:
            return 0  
    def patient_init(self,patient, need_random=0): 
        patient.infect_days = random.uniform(0.75,1.25) * self.infect_days
         
        if need_random:
            patient.b_random = True
            patient.sick_status = SICKSTATUS_SHOW # 有症狀...
             
            patient.sick_day= random.uniform(1,self.incubation_period[1]/2 + self.show_to_end[0])
            if random.uniform(0,1) <= self.show_to_heavy_rate:
                patient.sick_status = SICKSTATUS_HEAVY
            #print(patient.desc(0),end = '') #parser exception
    def desc(self,desc_id=0):
        txt_desc = "------ VirusModel Description: ------\n"
        desc_txt = txt_desc + "vm_mode=%i,vm_r0=%f, sickday_rnd=%f,infect_daystart=%i,incubation_period=%i %i,show_to_end=%i %i,infect_days=%i,show_to_heavy_rate=%f,infect_day_rate=%f" % (self.vm_mode,self.vm_r0,self.sickday_rnd,self.infect_daystart,self.incubation_period[0],self.incubation_period[1],self.show_to_end[0],self.show_to_end[1],self.infect_days,self.show_to_heavy_rate,self.infect_day_rate)
                

        return desc_txt