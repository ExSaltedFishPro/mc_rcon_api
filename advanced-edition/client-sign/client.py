from RconAPI import Sign
import requests
api_key = "XAS6NTiO2rTbE0Gl2W3nvQ"    
secret_key = "sHlQq5ZOjiXt44pPRClZPKmYZ7y37SYF2Lz7H_4VIbc"
api_url = "http://localhost:5003/api?"
command = "list"
sign = Sign()
url = sign.getRequestURL(api_key=api_key,api_url=api_url,secret_key=secret_key,command=command)
print(url)
input("")
print(requests.get(url).text)
