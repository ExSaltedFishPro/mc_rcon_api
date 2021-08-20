# mc_rcon_api
##一个简易的HTTP API以实现应用程序对RCON的访问

*在生产环境中请使用SSL，Flask原生<br>
##2021-8-20更新<br>
(./lite)适合api仅在内网的用户,去除了身份认证功能(未来可能会提供可选项)<br>
要求客户端采用GET方法在url中提供参数<br>
例如:http(s)://somedomain.x/api?command=x<br>

(./advanced-edition)提高了安全性能,适合API需要暴露在互联网中的用户<br>
采用了sqlite存储数据,要求客户端采用GET方法在url中提供参数<br>
鉴权需要api_key和secret_key,都存储在数据库中,generate_apikeys.py可一键生成<br>
例如:http(s)://somedomain.x/api?apikey=x&command=x&time=x&sign=x<br>
参数说明<br>
apikey : 存储在服务端auth.db中<br>
command : 需要执行的指令<br>
time : 当前时间截 #120s内有效<br>
sign : 鉴权签名<br>
    已经提供了一个Python模块(RconAPI.py)一键取得,也有一个例子进行手动计算(client_sample.py)<br>
    计算方法:  使用去除sign之后的URL参数串 <br>
    例：apikey=x&command=x&time=x<br>
    使用secret_key作为密钥，进行HMAC.sha256加密<br>
    将加密结果转换成字符串，再使用base64进行编码即得到签名<br>


##以下为网页简易版本(旧)(./webpage-edition)
#2021-8-4更新<br>
提供一个网页接口，如不需要可以选择删除部分函数。<br>

*需要依赖Flask<br>

项目包含一个服务端和一个客户端，请在启动服务端之前修改configs.json和auth.json<br>
auth.json包含API验证的信息(将来会使用加密)<br>
configs.json包含RCON需要的连接信息(将来会使用加密)<br>
<br>
客户端包含一个config.json，包含默认连接的API地址(需要启用请修改enabled=1)<br>

<br>服务端接受POST的类型的'authcode'   'mc_command'两个字段，验证失败返回'0x01',验证成功返回指令执行情况。
