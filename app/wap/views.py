from . import wap
from flask import render_template, redirect, request, url_for, flash, current_app, jsonify, abort
import os

import ssl
import base64
import time
import json
from urllib import request, parse
import hashlib
import requests


@wap.route('/')
def index():
    return render_template('wap/index.html')

@wap.route('/light/<state>')
def light(state):
    if state == 'on':
        os.system('/usr/bin/python3 /home/pi/python/jdq_on.py')
    else:
        os.system('/usr/bin/python3 /home/pi/python/jdq_off.py')
    return jsonify({'succ': 1, 'state': state})

@wap.route('/light/level/<level>')
def lightLevel(level):
    return jsonify({'succ': 1, 'state': level})

# 文字转语音
@wap.route('/voice/<text>')
def voice(text):
    r = requests.post(URL, headers=getHeader(), data=getBody(text))
    contentType = r.headers['Content-Type']
    print(contentType)
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        if AUE == "raw":
            print(r.content)
            fileName = '%s.wav' % str(int(time.time()))
            filePath = './app/static/audio/%s' % fileName
            writeFile(filePath, r.content)
            playAudio(fileName)
    else:
        print(r.text)
    return jsonify({'succ': 1})

# 每日问候语
@wap.route('/dayhello')
def dayHello():
    day = 'Vicky早上好，我是你的私人助理 狗蛋。。。'

    day += '今日天气：'
    weather = tuling('上海天气')
    day += weather + '。。。'

    day += '狗蛋给你讲个笑话：'
    joke = tuling('讲一个笑话')
    day += joke + '。'
    voice(day)
    return jsonify({'succ': 1})

# 讲个笑话吧

# 当前天气
@wap.route('/weather')
def weather():
    req = dayWeather()
    weather = json.loads(req)
    data = weather['data']
    city = data['city']
    forecast = data['forecast']
    weacherStr = city + ' '
    for i in range(len(forecast)):
        if i == 2:
            break
        weath = forecast[i]
        str = '今天' if i == 0 else '明天'
        weacherStr += str + weath['date'] + '  '
        weacherStr += '天气 ' + weath['type'] + '  '
        weacherStr += weath['high'] + '  '
        weacherStr += weath['low'] + '  '
        weacherStr += '      '

    voice(weacherStr)
    return jsonify({'succ': 1})

# 查询当日天气
def dayWeather():
    ssl._create_default_https_context = ssl._create_unverified_context
    params = parse.urlencode({'city': '上海'})
    url = 'https://www.apiopen.top/weatherApi'
    req = request.urlopen(url, params.encode('utf-8'))
    req = req.read().decode('UTF-8')
    return req

# 随机一个笑话
def dayJoke():
    pass

# 备忘录提醒
def memo():
    pass

# 每日开灯
def dayLightOn():
    pass

# 每日关灯
def dayLightOff():
    pass

# 图灵机器人
@wap.route('/tuling/<text>')
def tuling(text):
    userInfo = {'apiKey': '6d7cfb30e6d5463cbd5336cba25bbb6f', 'userId': '382554'}
    inputText = {'text': text}
    selfInfo = {'location': {'city': '上海'}}
    perception = {'inputText': inputText, 'selfInfo': selfInfo}
    dic = {'reqType': 0, 'perception': perception, 'userInfo': userInfo}
    req = request.Request('http://openapi.tuling123.com/openapi/api/v2')
    f = request.urlopen(req, json.dumps(dic).encode('utf-8'))
    dic = json.loads(f.read().decode('utf-8'))
    results = dic['results']
    if len(results) > 0:
        res = results[0]
        text = res['values']['text']
        return text
    return ''

# 播放音频
def playAudio(fileName):
    print('./app/static/audio/%s' % fileName)
    os.system('python %s/app/static/python/audio.py %s' % (os.path.abspath('.'), fileName))
    os.remove('./app/static/audio/%s' % fileName)

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5c46b533"
API_KEY = "86497a196738e10736f8322d9a43e168"
def getHeader():
    curTime = str(int(time.time()))

    param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"aisxping\",\"engine_type\":\"intp65\"}"
    print("param:{}".format(param))

    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))

    checkSum = m2.hexdigest()
    print('checkSum:{}'.format(checkSum))

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()