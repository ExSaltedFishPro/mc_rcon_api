import sqlite3
import secrets
api = secrets.token_urlsafe(16)
secret = secrets.token_urlsafe(32)
conn = sqlite3.connect("auth.db")
cur = conn.cursor()
cur.execute("insert into api_key (api,secret) values (?,?)",(api,secret))
conn.commit()
print("api_key:" + api)
print("secret_key" + secret)
conn.close()
input("")
