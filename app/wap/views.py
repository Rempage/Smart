from . import wap
from flask import render_template, redirect, request, url_for, flash, current_app, jsonify, abort
from .. import csrf
import os


@wap.route('/')
def index():
    return render_template('wap/index.html')

@wap.route('/light/<state>')
def light(state):
    return jsonify({'succ': 1, 'state': state})

@wap.route('/light/level/<level>')
def lightLevel(level):
    return jsonify({'succ': 1, 'state': level})