

def fileproess(file1,file2):
    """
    合并文件中的句子
    :return:
    """
    f = open(file1,'r',encoding='utf-8')
    f1 = open(file2,'w',encoding='utf-8')
    singlesentence =''
    singletag =''
    final = ''
    for line in f.readlines():
        print(line)
        sentence = line.split('   ')[0]
        tag = line.split('   ')[1]
        if '&&' in line:
            singlesentence = singlesentence+sentence
            singletag = singletag + tag.replace("\n","")
            final = final+singlesentence.replace('&&',"").replace('\t\n',"")+'\t'+singletag+'\n'
            f1.write(final)
            singlesentence = ''
            singletag = ''
            final = ''
        else:
            singlesentence = singlesentence + sentence
            singletag = singletag + tag.replace("\n", "")
    f.close()
    f1.close()