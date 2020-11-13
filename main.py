# -*- coding: utf-8 -*
import sys
from flask import Flask,request,jsonify
app=Flask(__name__)
import pickle
from Batch import BatchGenerator
from bilstm_crf import Model
import tensorflow as tf
from utils import *
from LAC import LAC
from util import proess
# from location.load_model import result_value
with open('./data/singlwordv3.pkl', 'rb') as inp:
    word2id = pickle.load(inp)
    id2word = pickle.load(inp)
    tag2id = pickle.load(inp)
    id2tag = pickle.load(inp)
    x_train = pickle.load(inp)
    y_train = pickle.load(inp)
    x_test = pickle.load(inp)
    y_test = pickle.load(inp)
    x_valid = pickle.load(inp)
    y_valid = pickle.load(inp)
print("train len:", len(x_train))
print("test len:", len(x_test))
print("word2id len", len(word2id))
print('Creating the data generator ...')
print('Finished creating the data generator.')
epochs = 31
batch_size = 32
config = {}
config["lr"] = 0.001  # learning rate
config["embedding_dim"] = 100
config["sen_len"] = len(x_train[0])
config["batch_size"] = batch_size
config["embedding_size"] = len(word2id) + 1
config["tag_size"] = len(tag2id)
config["pretrained"] = False

embedding_pre = []
print("begin to test...")
model = Model(config, embedding_pre, dropout_keep=1)
# text = request.get('text',type=str)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
ckpt = tf.train.get_checkpoint_state('./model1027v1')
path = ckpt.model_checkpoint_path
print('loading pre-trained model from %s.....' % path)
saver.restore(sess, path)

@app.route("/",methods=["POST"])
def Back():
    text = request.data.decode('utf-8')
    namesall = []
    for line in text.split('\n'):
        allnames = []
        for lin in line.split('。'):
            namelist = test_input1(lin, model, sess, word2id, id2tag, batch_size)
            for name in namelist:
                allnames.append(name)
        namesall.append(allnames)
    return jsonify({"data": namesall})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080',debug=True)
    sess.close()