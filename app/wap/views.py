from . import wap
from flask import render_template, redirect, request, url_for, flash, current_app, jsonify, abort
import os

import ssl
import uuid
import base64
import wave
import time
import sys

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.aai.v20180522 import aai_client, models


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

@wap.route('/voice/<text>')
def voice(text):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        cred = credential.Credential("AKIDIQXYkqVshRHAtUyGNLAwiOwJiBjr3raC", "kQ2fEcptnW5Y7YzNenpiedyDID5mGeu6")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "aai.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = aai_client.AaiClient(cred, "ap-shanghai", clientProfile)

        req = models.TextToVoiceRequest()

        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        params = '{"Text":"%s", "SessionId":"%s", "ModelType":%d, "Speed": 1}' % (text, suid, 1)
        req.from_json_string(params)

        resp = client.TextToVoice(req)
        decodeAndio = base64.b64decode(resp.Audio)

        fileName = '%s.wav' % str(int(time.time()))
        f = wave.open('./app/static/audio/%s' % fileName, 'wb')
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(decodeAndio)
        f.close()
        playAudio(fileName)
        return jsonify(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)
        return 'err'


def playAudio(fileName):
    os.system('python %s/app/static/python/audio.py %s' % (os.path.abspath('.'), fileName))
    os.remove('./app/static/audio/%s' % fileName)



