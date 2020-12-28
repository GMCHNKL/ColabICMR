import icmr
import Distripute
import sys
import basedir as bs

# python icmr_master.py start end (which instance)

datadict = []
resultData = bs.BaseDir+'DataRemains/ResultData.txt'
tag = icmr.file_exist(resultData)
print("Tag :",tag)
datadict = icmr.getDatadict(resultData)
print('lenth of datadict: ',len(datadict))
i = icmr.icmrProcess(datadict,tag,resultData)

try: split = int(sys.argv[3])
except: split = 1
Distripute.distripute_Data(split,'ResultData') 
# i.webCreation()
