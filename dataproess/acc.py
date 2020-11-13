import json
import sys
import dataproess1
import os
# def accscore(content,tag):
def countkey(tag):
    person_name = 0
    product_name = 0
    location = 0
    job_title = 0
    time = 0
    org_name = 0
    company_name = 0
    applist = []
    for i in tag:
        if i.strip() == 'person_name':
            person_name += 1
        if i.strip() == 'product_name':
            product_name += 1
        if i.strip() == 'location':
            location += 1
        if i.strip() == 'job_title':
            job_title += 1
        if i.strip() == 'time':
            time += 1
        if i.strip() == 'org_name':
            org_name += 1
        if i.strip() == 'company_name':
            company_name += 1
    applist.append(person_name)
    applist.append(product_name)
    applist.append(location)
    applist.append(job_title)
    applist.append(time)
    applist.append(org_name)
    applist.append(company_name)
    return applist

def acc_f1(f1,f2):
    file3 = open(f1, 'r', encoding='utf-8')
    allword = []
    for index2, f2line in enumerate(file3.readlines()):
        if f2line != '\n':
            json_data = json.loads(f2line)
            for i in json_data.values():
                allword.append(i)
    file1 = open(f2,'r',encoding='utf-8')
    taglist1 = []
    taglist = []
    for index,f1line in enumerate(file1.readlines()):
        word = f1line.split('\t')[0].strip()
        tag = f1line.split('\t')[1].replace("\n",'')
        if tag!='':
            if tag.endswith('*'):
                tag = tag[:-1]
            if tag is None:
                print(word,tag)
            else:
               # tagcount = len(tag.split('*'))
               for word1 in tag.split('*'):
                   tag1 = word1.split(':')[0]
                   taglist1.append(tag1)
                   word2 = word1.split(':')[1]
                   file2 = open(f1, 'r', encoding='utf-8')
                   for index2,f2line in enumerate(file2.readlines()):
                       if index==index2:
                           if f2line!='\n':
                              json_data = json.loads(f2line)
                              for jsonline in json_data.items():
                                  json_tag = jsonline[1]
                                  json_word = jsonline[0]
                                  if index==index2:
                                      if tag1==json_tag and word2==json_word:
                                          taglist.append(tag1)
                                          break
                   file2.close()
    f1all = countkey(allword)
    preall = countkey(taglist1)
    testall = countkey(taglist)
    f1 = []
    precision =[]
    for index,i in enumerate(testall):
        pre_person = float(int(i)/(int(preall[index])-int(i)))
        f1_preson = float(int(i)/(int(f1all[index])-int(i)))
        f1.append(f1_preson)
        precision.append(pre_person)
    for index2,i in enumerate(precision):
        if index2==0:
            print('pre_person_name:',precision[index2],'f1_person_name:',f1[index2])
        if index2==1:
            print('pre_product_name:',precision[index2],'f1_product_name:',f1[index2])
        if index2==2:
            print('pre_location:',precision[index2],'f1_location:',f1[index2])
        if index2==3:
            print('pre_job_title:',precision[index2],'f1_job_title:',f1[index2])
        if index2==4:
            print('pre_time:',precision[index2],'f1_time:',f1[index2])
        if index2==5:
            print('pre_org_name:',precision[index2],'f1_org_name:',f1[index2])
        if index2==6:
            print('pre_company_name:',precision[index2],'f1_company_name:',f1[index2])



if __name__ =='__main__':
    tempfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tempfile')
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    print(f1,f2)
    print(sys.argv)
    dataproess1.fileproess(f1,tempfile)
    acc_f1(f2,tempfile)