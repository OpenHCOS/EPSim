# @file simpy_eps.py
# @brief try code for simpy
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard
import collections
import random
#extend
import simpy
#library

RANDOM_SEED = 42
PATIENTS_START = 5  # Number of patients startup
PATIENTS_PERDAY = 0
BEDS_PER_HOSPITAL = 100
NURSE_COUNT = 10
SIM_TIME = 30  # Simulate until

class HospitalMgr():
    def __init__(self):
        #beds = simpy.Resource(env, capacity=10)
        self.hospitals = ['HsinChu', 'Taipei', 'Taichung']
        self.beds = {}
        self.nurses = {}
        self.num_renegers = 0
        for hos in self.hospitals:
            self.beds[hos] = simpy.Resource(env, capacity=BEDS_PER_HOSPITAL)
            self.nurses[hos] = simpy.Container(env, NURSE_COUNT, init=NURSE_COUNT)

        self.patients_gen_count = 0
        self.patients_served = 0
        self.patients_contacted = 0
    def desc(self,desc_id=0):
        desc_txt=""
        if self.patients_contacted>0:
            desc_txt = "served_rate=%.3f,patients_contacted=%i,patients_served=%i,num_renegers=%i\n" %(float(self.patients_served)/self.patients_contacted,self.patients_contacted,self.patients_served,self.num_renegers)
            for hos in self.hospitals:
                desc_txt+= "name=%s,used=%i,queues=%i\n" %(hos,self.beds[hos].count,len(self.beds[hos].queue))
        return desc_txt
def hospitalized(env, hm):
    """

    """
    hm.patients_contacted += 1
    
    queue_total=0
    for hos in hm.beds.keys():
        queue_total += len(hm.beds[hos].queue)
    
    if queue_total>BEDS_PER_HOSPITAL*3:
        hm.num_renegers += 1
        env.exit()        
    
    hos = random.choice(hm.hospitals)    
    days = random.randint(0, 5)
        
    with hm.beds[hos].request() as my_turn:
        result = yield my_turn

        hm.patients_served+=1
        yield env.timeout(days)
        


def patient_gen(env, hm, patient_count):
    for i in range(patient_count):
        env.process(patient_life(env, hm))
        
    
    while True:
        yield env.timeout(1) 
        for i in range(PATIENTS_PERDAY):    
            env.process(patient_life(env, hm))
    env.exit()
    
def patient_life(env, hm):
    hm.patients_gen_count += 1
    yield env.timeout(2) #潛伏期

    env.process(hospitalized(env, hm))
    
    for i in range(5): #每天傳染給一個人
        if random.uniform(0,1) < 2.2/5:
            env.process(patient_life(env, hm))
        yield env.timeout(1)
        



# Setup and start the simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()

hosmgr = HospitalMgr()

# Start process and run
env.process(patient_gen(env, hosmgr,PATIENTS_START))
for i in range(1,SIM_TIME):
    env.run(until=i)
    print("----- Day=%i -----" %(i))
    print(hosmgr.desc(0))
    

