import os, threading, ctypes
from functions import *

    
if not config['kopcheeka_api_key']:
    error('Input your kopeechka API key in the config.')
    

resp = httpx.get(f"http://api.kopeechka.store/user-balance?token={config['kopcheeka_api_key']}&api=2.0")
if 'OK' not in resp.text:
    error('Error getting kopeechka balance: ' + resp.json()['value'])
    time.sleep(3)
    quit()

balance = resp.json()['balance']

def update_headers():
    while True:
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(f"Tysm for purchasing this item :) |  Verified: {data.verified} | Claimed: {data.claimed} | Balance: {balance} RUB")
    
for i in range(1):
    threading.Thread(target = update_headers, daemon = True)
    
verify()
