import os
import os.path
from os import path
from os import listdir
from os.path import isfile, join
import sys
import basedir as bs

#python mergefiles.py level

def file_exist(resultData):
    if(path.exists(resultData) and readFile(resultData)==''):
        os.remove(resultData)
    return (path.exists(resultData))

def readFile(getfile):
    f = open(getfile,'r')
    fout = f.read()
    f.close()
    return fout

def writeFile(outStr,outfile):
    # outStr ='\n'.join(outStr)+'\n' if len(outStr)!=0 else ''
    f = open(outfile,'w')
    f.write(outStr)
    f.close()

def mergeFies(datafile='.txt',resfile='ResultData'):
    outstr = ''
    mypath = bs.BaseDir+'DataRemains'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and str(f).find(resfile)!=-1 and str(f).find(datafile)!=-1]
    for f in onlyfiles:
        f = join(mypath, f)
        outstr += readFile(f)
        os.remove(f)
    if len(onlyfiles)!=0:
        writeFile(outstr,join(mypath, resfile+'.txt'))

def merge(m):
    res = 'ResultData'
    res += '' if m=='0' else str(m)
    mergeFies(datafile='.txt',resfile=res)

if len(sys.argv)>1:
  merge(int(sys.argv[1]))

# mergeFies(datafile='s.txt',resfile='ResultData1')
# mergeFies(resfile='ResultData1.txt')