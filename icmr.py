import person
import xlrd
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import os.path
from os import path
from os import listdir
from os.path import isfile, join
import basedir as bs


def readFile(resultData):
    f = open(resultData,'r')
    fout = f.read()
    f.close()
    return fout

def writeFile(outStr,resultData):
    f = open(resultData,'w')
    f.write(outStr)
    f.close()

def file_exist(resultData):
    if(path.exists(resultData) and readFile(resultData)==''):
        os.remove(resultData)
    return (path.exists(resultData))

class icmrProcess():
    def __init__(self,datadict,tag,res):
        sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
        self.datadict = datadict
        self.uname = "GDHHNKTN"
        self.pas = "GDHHNKTN@icmr"
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        op.add_argument('--no-sandbox')
        op.add_argument('--disable-dev-shm-usage')
        self.br = webdriver.Chrome('chromedriver',chrome_options=op)
        self.personObject = []
        self.tag = tag
        self.res = res
        self.createEntries()

    def webCreation(self,new=False):
        
        self.br.get("https://cvstatus.icmr.gov.in/")
        person.wait()
        self.br.find_element_by_xpath('//*[@id="username"]').send_keys(self.uname)
        self.br.find_element_by_xpath('//*[@id="passwd"]').send_keys(self.pas)
        self.br.find_element_by_xpath('//*[@id="login_btn"]').click()
        self.enterAllData()

    def createEntries(self):
        print('createEntries')
        outStr = ''
        try:
            templist = []
            for j in self.datadict:
                print(j[0])
                p = person.register(j,self.br,self.tag)
                self.personObject.append(p)
                if not self.tag:
                    templist.append(p.getDataList())
                    outStr+=p.show()
            if not self.tag:
                self.datadict=templist
                writeFile(outStr,self.res)
            print('Finished')
        except Exception as e:
            print(e)
            
    
    def enterAllData(self):
        fout = readFile(self.res)
        count = 0
        remain = len(self.personObject)
        for p in self.personObject:
            count += 1
            print(str(count)+'.)')
            if p.enterValues():
                fout = fout.replace(p.show(),'')
                writeFile(fout,self.res)
                remain -= 1
            print('Remaining: '+str(remain))
        self.br.close()
        print("Execution Finished...... :)")

def getIndex(header,req):
    arr = []
    l = len(header)
    for i in req:
        try:
            elem = header.index(i) 
            arr.append(elem)  
        except:
            arr.append(l)
            l+=1
    return arr



def getXlData(fname,start=0,end=''):
    work = xlrd.open_workbook(fname)
    worksheet = work.sheet_by_index(0)
    cols = worksheet.ncols
    rows = worksheet.nrows
    itr = 0
    while (worksheet.cell(itr,0).value!='S.NO'):itr+=1
    table = []
    cols = getIndex([str(worksheet.cell(itr,i).value).strip() for i in range(cols)],['S.NO','COVID NUMBER','SAMPLE DATE','NAME',
    'AGE','SEX','COMPLETE ADDRESS','MOBILE NUMBER','RESULT','DATE OF RESULT','SRF ID','KIT USED','NG VALUE','RDRP VALUE'])
    print(cols)
    flag = False
    print('Row Count :',rows,'iter:',itr+1)
    for i in range(itr+1,rows):
        rowval = []
        try:
          # print('value',worksheet.cell(i,0).value)
          cno = int(worksheet.cell(i,0).value)
          if start<=cno and end>=cno:
            for j in cols:
                try:
                    data = worksheet.cell(i,j).value
                except: data=''
                if isinstance(data,float): data = int(data)
                rowval.append(str(data).rstrip().strip())
            table.append(rowval)
            if end==cno: break
        except Exception as e:
            print('line 130',e)
    return(table)

def getDatadict(resultData):
    mypath = bs.BaseDir+'DataFolder'
    print("file_exist(",resultData,") = ",file_exist(resultData))
    if not file_exist(resultData):
        print("listdir(mypath)=",listdir(mypath))
        datadict = []
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and not(f[0]=='~')]
        for file in onlyfiles:
            print('File Name: ', file)
            if len(sys.argv)<=1:
              start = int(input('Enter start : '))
              end = int(input('Enter end : '))
            else:
              try:
                start = int(sys.argv[1])
                end = int(sys.argv[2])
                if end==0:
                  end = 100000
              except:
                start = int(input('Enter start : '))
                end = int(input('Enter end : '))
            datadict.append(getXlData(bs.BaseDir+'DataFolder/'+file,start,end))
        datadict = [i for j in datadict for i in j]
        
    else:
        outStr = readFile(resultData)
        datadict=[[dt for dt in txt.split(';')] for txt in outStr.split('\n')]
        datadict.pop()
    return datadict

