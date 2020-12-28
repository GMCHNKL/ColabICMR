import os
from os import listdir
from os.path import isfile, join
from math import log
import sys 
import basedir as bs

mypath = bs.BaseDir+'DataRemains'

def readFile(getfile):
    f = open(getfile,'r')
    fout = f.read()
    f.close()
    return fout

def writeFile(outStr,outfile):
    outStr ='\n'.join(outStr)+'\n' if len(outStr)!=0 else ''
    f = open(outfile,'w')
    f.write(outStr)
    f.close()

def autodist(res):
    if res.find('.txt')==-1:
        res += '.txt'
    res = join(mypath, res)
    outStr = readFile(res)
    line = [i for i in outStr.split('\n')]
    line.pop()
    l = len(line)
    # print("line count :",l)
    div = (log(l)/log(2))
    return int(div)

def distripute_Data(n,res,form='{}'):
    resf = res+'.txt'
    if n<1: 
        n=autodist(resf)
    if n<=0:
        os.remove(join(mypath,resf))
        return
    outStr = readFile(join(mypath, resf))
    line = [i for i in outStr.split('\n')]
    line.pop()
    s = 0
    mid = (len(line)+1)//n
    m = mid
    for i in range(1,n):
        writeFile(line[s:m],str('{}/{}'+form+'.txt').format(mypath,res,str(i)))
        s = m
        m = m+mid
    writeFile(line[s:],str('{}/{}'+form+'.txt').format(mypath,res,str(n)))
    os.remove(join(mypath,resf))


if len(sys.argv)>1:
  if sys.argv[1]=='split':
    distripute_Data(int(sys.argv[2]),'ResultData')

# distripute_Data(2,'ResultData1')
# print(str('DataRemains\\{}'+'.{}s.'+'txt').format('res','str(i)'))
# n = autodist('DataRemains\\ResultData1.txt')
# print(n)
