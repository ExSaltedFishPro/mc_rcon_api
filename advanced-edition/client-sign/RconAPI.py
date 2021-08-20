import base64
import hmac
import time

class Sign():
    def getSign(self,secret_key:str,msg:str) -> str:
       """
       生成鉴权签名串
       """
       msg_encoded = msg.encode()
       secret = str.encode(secret_key)
       sign = hmac.new(secret,msg_encoded,digestmod="sha256")
       sign = sign.hexdigest()
       sign = str.encode(sign)
       sign_encoded = base64.b64encode(sign)
       sign_encoded = sign_encoded.decode()
       return sign_encoded
    def getRequestURL(self,api_key:str,secret_key:str,command:str,api_url:str)-> str:
        """
        一键取得URL\n
        URL示例:"http://example.com/api?"
        """
        timestamp = str(int(time.time()))
        msg = "apikey=" + api_key + "&" + "command=" + command + "&" + "time=" + timestamp
        sign = self.getSign(secret_key=secret_key,msg=msg)
        msg = msg + "&" + "sign=" + sign
        url = api_url + msg
        return url
