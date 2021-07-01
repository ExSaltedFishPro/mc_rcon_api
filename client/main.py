import requests
import json

#init
server = ""
auth = ""
build = 1
receive={}
data = {}
default=0

#load
with open('./configs/config.json','r',encoding='utf8')as cf:
    configs = json.load(cf)
if configs["enabled"]:
    server = configs["server"]
    auth = configs["auth"]

#function
def main():
    r = requests.get(server)
    receive = r.json()
    print(receive['API'])
    print(receive['Message'])
    print("使用“exit”退出程序")
    print("使用“logout”退出登录")
    while True:
        comm = input("/")
        if comm=="exit":
            quit()
        if comm=="logout":
            break
        data_send = {'authcode':auth,
                'mc_command':comm}
        a = requests.post(server,data = data_send)
        if a.text=="0x01":
            print("认证错误!")
            break
        print(a.text)


print("Minecraft Rcon API访问器")
print("版本1.1")

if configs["enabled"]:
    main()
while True:
    server = input("输入API地址:")
    auth = input("输入验证ID:")
    main()
