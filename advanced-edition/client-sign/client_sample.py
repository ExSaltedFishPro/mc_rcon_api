import requests
import base64
import hmac
import time

api_key = "XAS6NTiO2rTbE0Gl2W3nvQ"    
secret_key = "sHlQq5ZOjiXt44pPRClZPKmYZ7y37SYF2Lz7H_4VIbc"
api_url = "http://localhost:5003/api?"
command = "list"

secret_key = str.encode(secret_key)
timestamp = str(int(time.time()))

msg = "apikey=" + api_key + "&" + "command=" + command + "&" + "time=" + timestamp
msg = str.encode(msg)
sign = hmac.new(secret_key,msg,digestmod="sha256")
sign = sign.hexdigest()
sign = str.encode(sign)
sign_encoded = base64.b64encode(sign)
msg = msg.decode()

sign_encoded = sign_encoded.decode()
msg = msg + "&" + "sign=" + sign_encoded
url = api_url + msg
print(url)
print(requests.get(url).text)

input("")
