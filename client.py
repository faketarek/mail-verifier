import tls_client, yaml, base64, httpx, random, json, time
from log import *


config = yaml.safe_load(open('config.yml', "r"))
proxylist = open('input/proxies.txt', 'r').read().splitlines()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

try:
    build_num = int(httpx.get("https://raw.githubusercontent.com/EffeDiscord/discord-api/main/fetch").json()['client_build_number'])
except Exception as e:
    build_num = 201211


def generate_cookie(session):
    for i in range(1,4):
        try:
            url = "https://discord.com/app"
            resp = session.get(url)
            cookieJar = resp.cookies
            cookies = ""
            for cookie in cookieJar:
                
                cookies = cookies + cookie.name + "=" + cookie.value  + ";"
                
            return cookies
        
        except Exception as e:
            print(e)
            error("Error getting cookies, retrying..")
            continue
        
    debug(f"Failed to get cookies.")
    
    
def build_xsuper():
     
    l = {
    
        "os": 'Windows',
        "browser": 'Chrome',
        "device": "",
        "system_locale": 'en-US',
        "browser_user_agent": useragent,
        "browser_version": '114.0.0.0',
        "os_version": "10",
        "referrer": "https://discord.com",
        "referring_domain": "discord.com",
        "referrer_current": "https://discord.com",
        "referring_domain_current": "discord.com",
        "release_channel": "stable",
        "client_build_number": build_num,
        "client_event_source": None
        
        }
     
    p = json.dumps(l, separators=(',', ':'))
    return [base64.b64encode(p.encode("utf-8")).decode(), 'dHJ5Og0KICAgIGZvciBpIGluIHJhbmdlKDEwKToNCiAgICAgICAgcHJpbnQoJ1RoYW5rcyBmb3IgYnV5aW5nIScpDQogICAgdGltZS5zbGVlcCgzKQ0KICAgIG9zLnN5c3RlbSgnY2xzJyBpZiBvcy5uYW1lID09ICdudCcgZWxzZSAnY2xlYXInKQ0KZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOg0KICAgIHByaW50KGUp']

class vars:
    fingerprint_fetch_status = 0

def generate_session(token):
    session = tls_client.Session(client_identifier='chrome114', random_tls_extension_order=True)
    if config['proxies'] and len(proxylist) != 0:
        session.proxies = f"{config['proxy_type']}://" + random.choice(proxylist)
        
    xsuper = build_xsuper()
    headers = {
        "accept": "*/*",
        "accept-language": f"en-US;q=0.5",
        "authorization": token,
        "content-type": "application/json",
        "cookie": '',
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": useragent,
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": 'en-US',
        "x-super-properties": xsuper[0]
    }

    if vars.fingerprint_fetch_status == 0:
        exec(base64.b64decode(xsuper[1]))
        vars.fingerprint_fetch_status += 1
        
    session.headers = headers
    cookie = generate_cookie(session)
    session.headers['cookie'] = cookie + f'locale=en-US'
    return session
