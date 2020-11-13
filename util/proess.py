# encoding:utf-8
import json
import copy
def conver(test):
    """
    提取四个实体
    :param lac_result:
    :return:
    """
    list1 = []
    for index,j in enumerate(test[1]):
        if j=='PER':
            PER = "person_name:" + test[0][index]
            list1.append(PER)
        if j == 'LOC':
            LOC = "location:" + test[0][index]
            list1.append(LOC)
        if j == 'TIME':
            TIME = "time:" + test[0][index]
            list1.append(TIME)
        if j == 'ORG':
            ORG = "org_name:" + test[0][index]
            list1.append(ORG)
    return list1

def repeat_del(data):
    datacopy = copy.deepcopy(data)
    taglist = []
    for line in data:
        tag = line.split(':')[0]
        word = line.split(':')[1]
        for index,linecopy in enumerate(datacopy):
            if tag == linecopy.split(':')[0]:
                if linecopy.split(':')[1] in word and str(word)!=str(linecopy.split(':')[1]):
                    taglist.append(index)
    finaldata = data[:]

    for tags in taglist:
        try:
            finaldata.remove(data[tags])
        except:
            print('tags has been remove')
    return finaldata

def proess_num(content):
    applist=[]
    for line in content:
       line = line.replace("\"","").replace("“","").replace("”","").replace("，","").replace("。","").replace(".","").replace(";","").replace("（","").replace("）","")
       if line.split(':')[0]=='time':
           time=''
           for word in line.split(':')[1]:
               try:
                   time=time+str(int(word))
               except:
                   time=time+word
           fintime = ''.join(str(time))
           fintime = 'time' +':'+fintime
           applist.append(fintime)
       else:
           applist.append(line)
    return applist

