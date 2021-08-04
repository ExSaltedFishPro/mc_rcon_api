# mc_rcon_api
##一个简易的HTTP API以实现应用程序对RCON的访问

*这只是早期版本，未来版本会支持sqlite<br>
*在生产环境中请使用SSL，Flask原生<br>

#2021-8-4更新<br>
提供一个网页接口，如不需要可以选择删除部分函数。<br>

*需要依赖Flask<br>

项目包含一个服务端和一个客户端，请在启动服务端之前修改configs.json和auth.json<br>
auth.json包含API验证的信息(将来会使用加密)<br>
configs.json包含RCON需要的连接信息(将来会使用加密)<br>
<br>
客户端包含一个config.json，包含默认连接的API地址(需要启用请修改enabled=1)<br>

<br>服务端接受POST的类型的'authcode'   'mc_command'两个字段，验证失败返回'0x01',验证成功返回指令执行情况。
