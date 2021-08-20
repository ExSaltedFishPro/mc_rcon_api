# -*- coding: <utf-8> -*-
import time
from flask import *
from libs.rcon import MCRcon
import os
import json
import logging

with open('./conf/configs.json','r',encoding='utf8')as sc:
    server_configs = json.load(sc)
host = server_configs["host"]
password = server_configs["password"]
port = server_configs["port"]

def gettime():
    t = ''
    localtime = time.localtime(time.time())
    if localtime.tm_mon<10:
        t = str(localtime.tm_year)+'0'+str(localtime.tm_mon)+str(localtime.tm_mday)
    else:
        t = str(localtime.tm_year)+str(localtime.tm_mon)+str(localtime.tm_mday)
    return t
def create_response(code,info):
    response = '{"code":"' + code + '","info":"' + info + '"}'
    return response


logname = './log-' + gettime() + "-" + str(int(time.time())) + '.txt'
print("日志文件:" + logname)
logging.basicConfig(level=logging.NOTSET,
                    filename=logname,
                    filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
app = Flask(__name__)
@app.route('/api', methods=['GET'])
def api():
    command = request.args.get("command")
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    try:
        with MCRcon(host, password, port) as mcr:
            resp = mcr.command(command)
        code = "200"
    except:
        code = "201"
        resp = "无法连接到RCON"
        logging.error("Code" + code + ":" + resp)
    return create_response(code,resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
