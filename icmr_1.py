import icmr
import Distripute
import threading
import mergefiles as mf
from os import path
from os import listdir
from os.path import isfile, join
import mergefiles as mf
import sys
import basedir as bs


# pyhon icmr_1.py icmid (no.instance)

datadict = []
try: icmrid = str(sys.argv[1])
except: icmrid = str(input("ICMR ID: "))
myfolder = bs.BaseDir+'DataRemains'
resultData ='ResultData'+icmrid

class myThread (threading.Thread):
   def __init__(self, threadID, obj, res):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.res = res
      self.obj = obj
   def run(self):
      print ("Starting " , self.threadID)
      self.obj.webCreation()
      print ("Exiting " , self.threadID)
      tag = icmr.file_exist(myfolder+self.res)


threads = []
try:
   mf.merge(icmrid)
   mypath = bs.BaseDir+'DataRemains'
   try: n = int(sys.argv[2])
   except:
      n = Distripute.autodist(resultData)
   Distripute.distripute_Data(n,resultData,'.{}s')
   print('n=',n)
   onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and str(f).find(resultData)!=-1 and str(f).find('s.txt')!=-1]  
   print(onlyfiles)
   i = 0
   
   for f in onlyfiles:
      resf = myfolder+'/'+f
      i+=1
      datadict = icmr.getDatadict(resf)
      proc = icmr.icmrProcess(datadict,True,resf) 
      threads.append(myThread(i, proc, resf)) 

   for thread in threads:
      thread.start()

except Exception as e:
         print(e)

