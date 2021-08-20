# -*- coding: <utf-8> -*-
from flask import *
from libs.rcon import MCRcon
import os
import json
import sqlite3
import logging
import time
import hmac
import base64

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
with open('./conf/configs.json','r',encoding='utf8')as sc:
    server_configs = json.load(sc)
host = server_configs["host"]
password = server_configs["password"]
port = server_configs["port"]

app = Flask(__name__)
@app.route('/api', methods=['GET'])
def commander():
    conn = sqlite3.connect("auth.db")
    cur = conn.cursor()
    api_key = request.args.get('apikey')
    command = request.args.get('command')
    timestamp = request.args.get('time')
    sign = request.args.get('sign')
    try:
        sign = sign.encode()
        sign = base64.b64decode(sign)
    except:
        code = "205"
        resp = "请求错误"
        logging.warning(api_key + "Code" + code + ":" + resp)
        return create_response(code,resp)
    secret_key = cur.execute("select secret from api_key where api = (?)",(api_key,))
    try:
        secret_key = secret_key.fetchone()[0]
        conn.close()
    except:
        conn.close()
        code = "201"
        resp = "APIKEY不存在"
        logging.warning(api_key + ",Code" + code + ":" + resp)
        return create_response(code,resp)
    try:

        time_now = int(time.time())
        timestamp = int(timestamp)
    except:
        code = "205"
        resp = "请求错误"
        logging.warning(api_key + ",Code" + code + ":" + resp)
        return create_response(code,resp)
    if time_now - timestamp>120:
        code = "202"
        resp = "请求超时,时间截认证失败"
        logging.warning(api_key + ",Code" + code + ":" + resp)
        return create_response(code,resp)
    msg = "apikey=" + api_key + "&" + "command=" + command + "&" + "time=" + str(timestamp)
    secret_key = str(secret_key)
    secret_key_encoded = str.encode(secret_key)
    msg = str.encode(msg)
    try:
        sign_verify = hmac.new(secret_key_encoded,msg,digestmod="sha256")
        sign_verify = sign_verify.hexdigest()
        sign = sign.decode()
    except:
        code = "203"
        resp = "签名鉴权失败"
        logging.warning(api_key + ",Code" + code + ":" + resp)
        return create_response(code,resp)
    try:
        if hmac.compare_digest(sign,sign_verify)==False:
            code = 203
            resp = "签名鉴权失败"
            logging.warning(api_key + ",Code" + code + ":" + resp)
            return create_response(code,resp)
    except:
        code = "203"
        resp = "签名鉴权失败"
        logging.warning(api_key + ",Code" + code + ":" + resp)
        return create_response(code,resp)
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    try:
        with MCRcon(host, password, port) as mcr:
            resp = mcr.command(command)
    except:
        code = "204"
        resp = "RCON离线"
        logging.error(api_key + ",Code" + code + ":" + resp)
        return create_response(code,resp)
    code = "200"
    logging.info(api_key + ",Code" + code + ":" + command + ":" + resp)
    return create_response(code,resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5003)
