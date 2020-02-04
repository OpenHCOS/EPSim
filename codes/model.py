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
import copy
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####


#Spec: Manager the model, collect the history
#How/NeedToKnow:
class ModelMgr():
    def __init__(self):
        self.history_x = []
        self.pms = [] # PatientMgrs

    #def append(self,data_date, pm, mr):
    def append(self,model):
        data_date = model.dt_end
        pm = model.patient_mgr
        pm.update_day_usage()
        self.history_x.append(data_date)
        self.pms.append(copy.deepcopy(pm))
    def pms_info(self,info_id=0):
        info = []
        if info_id==0: # default, return all patients count
            for pm in self.pms:
                info.append(len(pm.patients))
        if info_id==1:
            for i in range(len(self.pms)):
                if i==0:
                    rate = len(self.pms[0].patients) / float(gc.SETTING["PATIENT_START_COUNT"])
                    info.append(rate)
                elif i< len(self.pms)-1:
                    info.append(float(len(self.pms[i+1].patients))/ len(self.pms[i].patients))
                    
        return info
    def desc(self,desc_id=0):
        # 0 - console
        # 1 - file
        if desc_id==0:
            txt_desc = "------ ModelMonitor Description: ------\n"
        else:
            txt_desc = ""
        for i in range(len(self.pms)):
            pm = self.pms[i]
            if i == 0 :
                keys = "date,patient,pass,die,init,show,heavy"
                for key in pm.day_usage.keys():
                    keys += "," + key
                txt_desc += keys + "\n"
            vstr = ""
            for key in pm.day_usage.keys():
                vstr += "," + "%.2f" %(pm.day_usage[key])
            status = pm.rpt_status()
            txt_desc += "%s,%i,%i,%i,%i,%i,%i%s\n" %(self.history_x[i].strftime('%Y-%m-%d'), len(pm.patients),len(pm.p_pass),len(pm.dies),status[0],status[1],status[2],vstr)
        return txt_desc

#Spec: Core simulation model
#How/NeedToKnow:
class Model():
    def __init__(self,env):
        #private
        #global: these variables allow to direct access from outside.
        self.reset(env)
        
        
    def reset(self,env):
        self.env = env
                
        fmt = '%Y-%m-%d'
        self.dt_start = datetime.strptime(gc.SETTING["MODEL_START_TIME"], fmt)
        self.dt_end = self.dt_start #init value
        
        
        self.patient_mgr = PatientMgr() 
        #self.patient_mgr.start_init()
        self.srs= StateRecordSets()
        #sr = self.srs.find_byoffset(0) 
        #self.patient_mgr.update_sr(sr)
        
        self.model_desc = ""
        self.model_day=0
        
        
        
        
    def model_setup(self):
        self.env.process(self.patients_run()) 
    
    def patients_run(self):
        rate_prev = 1.0
        while True:
            die_list = []
            pass_list = []
            
            
            for k in list(self.patient_mgr.patients):
                p = self.patient_mgr.patients[k]
                gc.VIRUS.age_oneday(p)
                if p.sick_status == SICKSTATUS_DIE:
                    die_list.append(k)
                    
                if p.sick_status==SICKSTATUS_PASS:
                    pass_list.append(k)
            
                inf_rate = gc.VIRUS.infect_byday(p)
                if random.uniform(0,1) < inf_rate: # 感染新病人
                    self.patient_mgr.add_patient(p.p_seq,self.model_day)
                    p.infect_count+=1
            for n in die_list:
                self.patient_mgr.dies[n] = self.patient_mgr.patients[n]
                del self.patient_mgr.patients[n]
                
            for n in pass_list:
                self.patient_mgr.p_pass[n] = self.patient_mgr.patients[n]
                del self.patient_mgr.patients[n]
                #self.patient_mgr.add_sr5()
            #logging.info("patients count %i" %(len(self.patient_mgr.patients)))
            
            # cal diff

            if gc.VIRUS.dr0_enable:
                date = gc.MODEL.dt_start + timedelta(self.model_day)
                v_set = self.srs.find_record_by_date(date)
                
                if v_set == -1: # have valid value
                    rate = rate_prev
                else:
                    rate = v_set/len(self.patient_mgr.patients)
                    rate_prev = rate
                gc.VIRUS.dr0 = 1.0 - gc.VIRUS.pid.update(rate)
                print("txt_date = %s, model_day=%i,value=%i,rate=%f,dr0=%f" %(date,self.model_day,v_set,rate,gc.VIRUS.dr0))
                
            yield self.env.timeout(1)  
        
    def desc(self,desc_id):
        return self.patient_mgr.desc(desc_id)
