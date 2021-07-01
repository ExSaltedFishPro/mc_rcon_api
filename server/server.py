# -*- coding: <utf-8> -*-
from flask import Flask
import readline
import getopt
import sys
import re
from libs.rcon import MCRcon
import os
import json
from flask import request

#init
global auth_ok
host = ""
password = ""
port = int()
authlist = []  
server_configs = {}
temp_dict = {}

#load
with open('./conf/configs.json','r',encoding='utf8')as sc:
    server_configs = json.load(sc)
host = server_configs["host"]
password = server_configs["password"]
port = server_configs["port"]
with open('./conf/auth.json','r',encoding='utf8')as au:
    authlist = json.load(au)

app = Flask(__name__)
@app.route('/')
def index():
    return '404 NOT FOUND'

@app.route('/command', methods=['POST'])
def commander():
    auth_ok = 0
    authc = request.values.get('authcode')
    command = request.values.get('mc_command')
    for i in authlist:
        if authc == i:
            auth_ok = 1
    if auth_ok != 1:
        return '0x01'
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    with MCRcon(host, password, port) as mcr:
        resp = mcr.command(command)
    return resp
@app.route('/command', methods=['GET'])
def version():
    data = {}
    data = {'API_Version':'1.1',
            'Description':'A MC RCON REMOTE API',
            'API':'MCRCON_API_TEST_V1.1',
            'Message':'Welcome'}
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
