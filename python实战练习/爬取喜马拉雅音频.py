import requests
url='https://audiopay.cos.tx.xmcdn.com/download/1.0.0/storages/83ae-audiopay/1F/3F/GKwRIJII6EdLAC3NsgJhEFTt-aacv2-48K.m4a?sign=1ac2fb8a53a96fd7415c0047d163a983&buy_key=FM&timestamp=1763003206072000&token=6861&duration=370'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
}
resp=requests.get(url,headers=headers)
with open('templates/audio/1.mp3', 'wb') as f:
    f.write(resp.content)