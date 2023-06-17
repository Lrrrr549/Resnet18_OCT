import flask
from flask import Flask,request,render_template
from resnet_load import pre_OCT
import gevent
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
import os
import shutil
# from chest_fun import chest_pre

from keras.models import load_model
import numpy as np
from PIL import Image
from keras import backend as K
import tensorflow as tf
from tensorflow import image

path = '/home/lighthouse/resnet-OCT/resnet50-NIH/00000001_001.png'

label14_cn =['肺不张','心脏扩大','肺实变','水肿','积液','肺气肿',
                '纤维化','疝气','浸润','肿块','结节','胸膜增厚','气胸','肺炎']

app = Flask(__name__)
model_path = '/home/lighthouse/resnet-OCT/OCT-Resnet_model.pth'

@app.route("/OCT", methods=['GET'])
def oct():
    return render_template('OCT.html')

@app.route("/Chest", methods=['GET','POST'])
def chest():
    return render_template('chest.html')

@app.route("/OCT_pre", methods=['GET','POST'])
def pre():
    if request.method == 'POST':
        # 获得上传文件及文件名称
        f = request.files['file']
        filename = secure_filename(f.filename)
        print(filename)

        # 保存文件
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'upload', filename)
        f.save(file_path)

        print("----Start predict----")
        # pre_OCT(model_path, img_path)
        pre_name = pre_OCT(model_path, file_path)
        # shutil.rmtree('/home/lighthouse/resnet-OCT/upload')
        # os.makedirs('/home/lighthouse/resnet-OCT/upload')
        return pre_name
    return None

'''
@app.route("/chest_pre", methods=['GET','POST'])
def chest_pre():
    if request.method == 'POST':
        # 获得上传文件及文件名称
        f = request.files['file']
        filename = secure_filename(f.filename)
        print(filename)

        # 保存文件
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'upload', filename)
        f.save(file_path)
        print(file_path)
        print("----Start predict----")
        # path = '/home/lighthouse/resnet-OCT/resnet50-NIH/00000001_001.png'
        # print(pre)
        return pre
    return None

'''

@app.route("/index", methods=['GET'])
def index2():
    return render_template("index.html")


if __name__ == '__main__':
    # port=5000
    #app.run('0.0.0.0',port=5000,debug=True)
    http_server = WSGIServer(('0.0.0.0', 5000),app)
    http_server.serve_forever()


