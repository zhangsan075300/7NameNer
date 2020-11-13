# coding=utf-8
import codecs
import re
import numpy as np
# import jieba

def calculate1(x, y, id2word, id2tag, res=[]):
    entity = []
    for i in range(len(x)):  # for every sen
        for j in range(len(x[0])):  # for every word
            if x[i][j] == 0 or y[i][j] == 0:
                continue
            if id2tag[y[i][j]][0] == 'B':
                entity = [id2word[x[i][j]] + '/' + id2tag[y[i][j]]]
            elif id2tag[y[i][j]][0] == 'I' and len(entity) != 0 and entity[-1].split('/')[1][1:] == id2tag[y[i][j]][1:]:
                entity.append(id2word[x[i][j]] + '/' + id2tag[y[i][j]])
            elif id2tag[y[i][j]][0] == 'I' and len(entity) != 0 and entity[-1].split('/')[1][1:] == id2tag[y[i][j]][1:]:
                entity.append(id2word[x[i][j]] + '/' + id2tag[y[i][j]])
                entity.append(str(i))
                entity.append(str(j))
                res.append(entity)
                entity = []
            else:
                entity = []

    return res
def calculate(x, y, id2word, id2tag, res=[]):
    entity = []
    for i in range(len(x)):  # for every sen
        for j in range(len(x[0])):
            try:# for every word
                if x[i][j] == 0 or y[i][j] == 0:
                    continue
                if id2tag[y[i][j]][0] == 'B':
                    entity = [id2word[x[i][j]] + '/' + id2tag[y[i][j]]]

                elif id2tag[y[i][j]][0] == 'I' and len(entity) != 0 and entity[-1].split('/')[1][1:] == id2tag[y[i][j]][1:]:
                    entity.append(id2word[x[i][j]] + '/' + id2tag[y[i][j]])

                    entity.append(str(i))
                    entity.append(str(j))
                    res.append(entity)
                else:
                    entity = []
            except:
                pass
    # print("res:",res)
    return res

def get_entity(x, y, id2tag):
    entity = ""
    res = []
    for i in range(len(x)):  # for every sen
        for j in range(len(x[0])):  # for every word
            if y[i][j] == 0:
                continue
            if id2tag[y[i][j]][0] == 'B':
                entity = id2tag[y[i][j]][2:] + ':' + x[i][j]
            elif id2tag[y[i][j]][0] == 'I' and len(entity) != 0:
                entity += x[i][j]
                res.append(entity)
            # elif id2tag[y[i][j]][0] == 'I' and len(entity) != 0:
            #     print("11111111111111111111111")
            #     entity += x[i][j]
            #     res.append(entity)
            #     entity = []
            else:
                entity = []

    return res


def write_entity(outp, x, y, id2tag):
    '''
    注意，这个函数每次使用是在文档的最后添加新信息。
    '''
    entity = ''
    res = []
    for i in range(len(x)):
        if y[i] == 0:
            continue
        if id2tag[y[i]][0] == 'B':
            entity = id2tag[y[i]][2:] + ':' + x[i]
        elif id2tag[y[i]][0] == 'I' and len(entity) != 0:
            entity += x[i]
            res.append(entity)
        # elif id2tag[y[i]][0] == 'E' and len(entity) != 0:
        #     entity += x[i]
        #     outp.write(entity + ' ')
        #     entity = ''
        else:
            entity = ''
    namelist = []

    for index in range(len(res) - 1):
        if res[index].split(":")[0] != res[index + 1].split(":")[0]:
            namelist.append(res[index])
    try:
        namelist.append(res[-1])
    except:
        pass
    for name in namelist:
        outp.write(name+'*')

    return

def train(model, sess, saver, epochs, batch_size, data_train, data_test, id2word, id2tag):
    batch_num = int(data_train.y.shape[0] / batch_size)
    batch_num_test = int(data_test.y.shape[0] / batch_size)
    for epoch in range(epochs):
        for batch in range(batch_num):
            x_batch, y_batch = data_train.next_batch(batch_size)
            # print x_batch.shape
            feed_dict = {model.input_data: x_batch, model.labels: y_batch}
            pre, _ = sess.run([model.viterbi_sequence, model.train_op], feed_dict)
            acc = 0
            if batch % 200 == 0:
                for i in range(len(y_batch)):
                    for j in range(len(y_batch[0])):
                        if y_batch[i][j] == pre[i][j]:
                            acc += 1
                print(float(acc) / (len(y_batch) * len(y_batch[0])))
        path_name = "./model1030v2/model" + str(epoch) + ".ckpt"
        print(path_name)
        if epoch % 3 == 0:
            saver.save(sess, path_name)
            print("model has been saved")
            entityres = []
            entityall = []
            for batch in range(batch_num):
                x_batch, y_batch = data_train.next_batch(batch_size)
                feed_dict = {model.input_data: x_batch, model.labels: y_batch}
                pre = sess.run([model.viterbi_sequence], feed_dict)
                pre = pre[0]
                entityres = calculate(x_batch, pre, id2word, id2tag, entityres)
                entityall = calculate(x_batch, y_batch, id2word, id2tag, entityall)
            jiaoji = [i for i in entityres if i in entityall]
            if len(jiaoji) != 0:
                zhun = float(len(jiaoji)) / len(entityres)
                zhao = float(len(jiaoji)) / len(entityall)
                print("ture postive number:",len(jiaoji))
                print("actually postive number:",len(entityres))
                print("original postive number:",len(entityall))
                print("train")
                print("formulapre:", str(len(jiaoji)) + '/' + str(len(entityres)) + ',P=(TP/TP+FP)')
                print("formularec:", str(len(jiaoji)) + '/' + str(len(entityall)) + ',R=(TP/TP+FN)')
                print("formulaf1:", str((2 * zhun * zhao)) + '/' + str((zhun + zhao)) + ',(2*P*R/P+R)')
                print("precision:", zhun)
                print("recall:", zhao)
                print("f1:", (2 * zhun * zhao) / (zhun + zhao))
            else:
                print("precision:", 0)
            entityres = []
            entityall = []
            for batch in range(batch_num_test):
                x_batch, y_batch = data_test.next_batch(batch_size)
                feed_dict = {model.input_data: x_batch, model.labels: y_batch}
                pre = sess.run([model.viterbi_sequence], feed_dict)
                pre = pre[0]
                entityres = calculate(x_batch, pre, id2word, id2tag, entityres)
                entityall = calculate(x_batch, y_batch, id2word, id2tag, entityall)
            jiaoji = [i for i in entityres if i in entityall]
            if len(jiaoji) != 0:
                zhun = float(len(jiaoji)) / len(entityres)
                zhao = float(len(jiaoji)) / len(entityall)
                print("ture postive number:", len(jiaoji))
                print("actually postive number:", len(entityres))
                print("original postive number:", len(entityall))
                print("test")
                print("formulapre:", str(len(jiaoji)) + '/' + str(len(entityres)) + ',P=(TP/TP+FP)')
                print("formularec:", str(len(jiaoji)) + '/' + str(len(entityall)) + ',R=(TP/TP+FN)')
                print("formulaf1:", str((2*zhun*zhao)) + '/' + str((zhun + zhao))+',(2*P*R/P+R)')
                print("precision:", zhun)
                print("recall:", zhao)
                print("f1:", (2 * zhun * zhao) / (zhun + zhao))
            else:
                print("precision:", 0)
max_len = 60
def padding(ids):
    if len(ids) >= max_len:
        return ids[:max_len]
    else:
        ids.extend([0] * (max_len - len(ids)))
        return ids


def padding_word(sen):
    if len(sen) >= max_len:
        return sen[:max_len]
    else:
        return sen

def padding_word1(sen):
    if len(sen)+2 >= max_len:
        return sen[:max_len-2]+'&&'
    else:
        return sen+'&&'


def test_input1(text,model, sess, word2id, id2tag, batch_size):
    while True:
        text = re.split(u'[！？、‘’“”（）]', text)
        print(text)
        text_id = []
        text1 = []
        for sen in text:
            word_id = []
            for word in sen:
                if word in word2id:
                    word_id.append(word2id[word])
                else:
                    word_id.append(word2id["unknow"])
            text_id.append(padding(word_id))
            text1.append(padding_word(sen))
        zero_padding = []
        zero_padding.extend([0] * max_len)
        text_id.extend([zero_padding] * (batch_size - len(text_id)))
        feed_dict = {model.input_data: text_id}
        pre = sess.run([model.viterbi_sequence], feed_dict)
        entity = get_entity(text1, pre[0], id2tag)
        namelist = []
        for index in range(len(entity) - 1):
            if entity[index].split(":")[0] != entity[index + 1].split(":")[0]:
                namelist.append(entity[index])
                # print(namelist)
        try:
            namelist.append(entity[-1])
        except:
            print('e')
        return namelist

def test_input(model, sess, word2id, id2tag, batch_size):
    while True:
        text = input("请输入text")
        text = re.split(u'[，。！？、‘’“”（）]', text)
        text_id = []
        for sen in text:
            word_id = []
            for word in sen:
                print(word)
                if word in word2id:
                    word_id.append(word2id[word])
                else:
                    word_id.append(word2id["unknow"])
            text_id.append(padding(word_id))

        zero_padding = []
        zero_padding.extend([0] * max_len)
        text_id.extend([zero_padding] * (batch_size - len(text_id)))
        feed_dict = {model.input_data: text_id}
        pre = sess.run([model.viterbi_sequence], feed_dict)
        entity = get_entity(text, pre[0], id2tag)
        namelist = []
        for index in range(len(entity)-1):
            if entity[index].split(":")[0] != entity[index+1].split(":")[0]:
                namelist.append(entity[index])
        namelist.append(entity[-1])
        print(namelist)
        # namelist = []
        # for i in entity:
        #     namelist.append(i)
        # print(namelist)


def extraction(input_path, output_path, model, sess, word2id, id2tag, batch_size):
    text_id = []
    text = []
    with codecs.open(input_path, 'rb', 'utf-8') as inp:
        count=0
        for line in inp.readlines():
            line =line.replace("$$",'').replace("\n","").replace(' ','')
            count+=1
            line = re.split('[。！？、‘’“”（）]', line.strip())
            while '' in line:
                line.remove('')
            for index2,sentence in enumerate(line):
                if sentence == '' or sentence == ' ':
                    continue
                word_id = []
                for word in sentence:
                    if word in word2id:
                        word_id.append(word2id[word])
                    else:
                        word_id.append(word2id["unknow"])
                text_id.append(padding(word_id))

                if index2 == len(line)-1:
                    text.append(padding_word1(sentence))
                else:
                    text.append(padding_word(sentence))
    # print("text_id2:",text_id)
    print("text_id2:", np.asarray(text_id).shape)
    zero_padding = []
    zero_padding.extend([0] * max_len)
    text_id.extend([zero_padding] * (batch_size - len(text_id) % batch_size))
    print("text_id1:", np.asarray(text_id).shape)
    # print("text_id1:",text_id)
    text_id = np.asarray(text_id)
    text_id = text_id.reshape(-1, batch_size, max_len)
    print("text_id3:", text_id.shape)

    predict = []
    for index in range(len(text_id)):
        feed_dict = {model.input_data: text_id[index]}
        pre = sess.run([model.viterbi_sequence], feed_dict)
        predict.append(pre[0])
    predict = np.asarray(predict).reshape(-1, max_len)
    with codecs.open(output_path, 'a', 'utf-8') as outp:
        for index in range(len(text)):
            outp.write(text[index] + "   ")
            write_entity(outp, text[index], predict[index], id2tag)
            outp.write('\n')

def extracphone(phone):

    a= re.compile('(1)-?([0-9]{3}) ?([0-9]{7})')
    res = ','.join([''.join(ele) for ele in a.findall(phone)])
    return res



def extracemail(email):
    a = re.findall('[0-9a-zA-Z_\.]{1,19}@[0-9a-zA-Z\.]{1,13}\.[com,cn,net,mil]{1,3}', email)
    return ','.join([str(i) for i in a])