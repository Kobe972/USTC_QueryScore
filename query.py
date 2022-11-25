from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask import Flask,request,send_file,render_template
import requests
import io
import numpy as np
scores=[]
with open('data.txt','r',encoding='utf-8') as fp:
    lines=fp.readlines()
for line in lines:
    scores.append([line.split(' ')[0],float(line.split(' ')[-1])])
raw_scores=np.array(scores)
scores=np.array(scores)
index=np.argsort(scores[:,1].astype(np.float32))
rank=np.argsort(index)
scores[:,1]=(scores[:,1].astype(np.float32)-np.min(scores[:,1].astype(np.float32)))/(np.max(scores[:,1].astype(np.float32))-np.min(scores[:,1].astype(np.float32)))
rank=rank/np.max(rank)
raw_scores=np.concatenate((raw_scores,(1-rank[None,:].T)*100),axis=1)
scores[:,1]=scores[:,1].astype(np.float32)*0.3+rank*0.7
scores[:,1]=(scores[:,1].astype(np.float32)-np.min(scores[:,1].astype(np.float32)))/(np.max(scores[:,1].astype(np.float32))-np.min(scores[:,1].astype(np.float32)))
app=Flask(__name__)
SHA_TZ=timezone(
    timedelta(hours=8),
    name='Aisa/Shanghai'
)
@app.route('/',methods=['GET'])
def index():
    response=render_template('index.html')
    return response
@app.route('/grayscale',methods=["GET"])
@app.route('/grayscale/',methods=["GET"])
def grayscale():
    global scores
    auth = request.args.get("auth")
    auth=requests.get('http://qq.ustc.life/p/'+auth).text
    if '学号（或教工号）：' in auth:
        pos=auth.find('学号（或教工号）：')
        auth=auth[pos+len('学号（或教工号）：'):]
        pos=auth.find('</p>')
        auth=auth[:pos]
        pixel=(1-float(scores[scores[:,0]==auth][0,1]))*255
        result=np.ones((100,100))*pixel
        frame=cv2.cvtColor(result.astype(np.float32),cv2.COLOR_GRAY2RGB)
        b_img = cv2.imencode('.png', frame)[1].tobytes()
        return send_file(
        io.BytesIO(b_img),
        mimetype='image/png',
        as_attachment=True,
        download_name='grayscale.png')
@app.route('/obscure',methods=["GET"])
@app.route('/obscure/',methods=["GET"])
def obscure():
    response=render_template('obscure.html')
    return response
@app.route('/accurate',methods=["GET"])
@app.route('/accurate/',methods=["GET"])
def accurate():
    enable=True #如未开放准确查分，设为False
    if not enable:
        response=render_template('disabled.html')
        return response
    global raw_scores
    global scores
    auth = request.args.get("auth")
    auth=requests.get('http://qq.ustc.life/p/'+auth).text
    if '学号（或教工号）：' in auth:
        pos=auth.find('学号（或教工号）：')
        auth=auth[pos+len('学号（或教工号）：'):]
        pos=auth.find('</p>')
        auth=auth[:pos]
        score=raw_scores[scores[:,0]==auth][0]
        result='<p>StuId:'+score[0]+'</p>'
        result+='<p>Score:'+score[1]+'</p>'
        result+='<p>Rank:'+score[2]+'%</p>'
        return result
    response=render_template('index.html')
    return response
app.run(host="0.0.0.0",port=80,debug=False,threaded=True)

