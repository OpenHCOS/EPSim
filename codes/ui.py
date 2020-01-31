# @file ui.py
# @brief 
# README: User interface related, import/export
# MODULE_ARCH:  
# CLASS_ARCH:
# GLOBAL USAGE: 
#standard

#extend
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#library
import lib.globalclasses as gc
from lib.const import *

##### Code section #####
#Spec: plot
#How/NeedToKnow:
class UserInterface():
    def __init__(self):
        #private
        #global: these variables allow to direct access from outside.
        self.plot_seq=0
        pass
      
    def test(self,data_x,data,label):
        plt.xlabel('Date')
        plt.ylabel('Patients Count')
        p = plt.plot(data,label=label)
        #p = plt.plot(data_x,data,label=label)
        #plt.plot_date(data_x,data,label=label)
        
        plt.legend()
        #locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        
        #mdates.ConciseDateFormatter
        #mdates.Con
        #formatter = mdates.DateFormatter("%Y/%m/%d")
        
        #p.xaxis.set_major_locator(locator)
        #p.xaxis.set_major_formatter(formatter)
        
        
        
        filename = "output/figure-%i.png" %(self.plot_seq)
        plt.savefig(filename)
        self.plot_seq+=1
        plt.close()
        #plt.show()
        
            
