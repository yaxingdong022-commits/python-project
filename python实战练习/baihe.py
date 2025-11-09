import requests
import re
from urllib.request import urlretrieve
#用来下载图片的包
url='https://search.baihe.com/search/getUserList?userIDs=139452612,142843004,143996345,143235614&jsonCallBack=jQuery18303401046398715697_1762150309765'
headers={
    'Cookie':'accessID=20251103123421548630; cookie_pcc=701%7C%7Cwww.baidu.com%7C%7C%7C%7Chttps%3A//www.baidu.com/link/url%3D0pHQsVpt0ruKpkYZ0HbjM0KZNd_j6oum-oNjaa3y2VG%26wd%3D%26eqid%3D9c2a56fe000044e300000003690830f1; tempID=0616415413; AuthCookie=4BFFD62B611D896EB34D665E7A26B9971639A95FC67B522CC66CC416E52650CAC6E5940F3A828C4B904AF051C2A81FF4D7A6E2425F8EA858763EB29E597C153A7A57DAA6B9D742FC6BFB0F813A653583; AuthMsgCookie=A8BB4C22F7E5B0A4D0409C99D4532235B7A5B6A3909609C7E78D3D2876E56D6CA2412A55DB0356732493AAB7AA835C166A026473AD9412A2F84BD966CED7DAFFB19A84AB949FA1481DD3A2C29CC25F11; GCUserID=397600755; OnceLoginWEB=397600755; userID=397600755; spmUserID=397600755; AuthSlviCookie=839D5191D89B9C12811A7C05A6168C07DEC5D01661F82F47F31868590DAE1AA212796668666D8F2742E514F06947BFB6A1FDA43F1EDF45011AA7A341CAE94619B71F1C25ED4FE8448CC5553C427BED3E7DD50068AC4F92AB77F9ECA3EABB4CCD; setIp=1; orderSource=10130301; AuthCheckStatusCookie=14CE9451151C3A4C6A0BC714DCE2BFC914D1D3015978705726A127B203C4931405E9D878DCC812E7; deviceid2=09fb8123-ef2f-45ec-842c-6e06c6f3f2e4; deviceid2=6d070727-fee8-485b-80b5-7e3917165165; accessToken=BH1762150027301292741; lastLoginDate=2025-11-03+14%3A07%3A47; AuthTokenCookie=bh.1762150068270_1800.331C82C45D90D3A55116971322F91479C3863105.bhqUi7p.6; Hm_lvt_5caa30e0c191a1c525d4a6487bf45a9d=1762144462,1762150029; Hm_lpvt_5caa30e0c191a1c525d4a6487bf45a9d=1762150029; HMACCOUNT=81E042B755412016; _fmdata=weZq%2FWaRF%2ByqigmBK0ph0st%2Fz1pivJsU7FKHnihCv9pCweMW%2FeljtoN606y5a038acSpM0i9Mpp%2BqL0qliSP7JPM2MC60kRTN1Eoz4PH6J8%3D',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0'
}
resp=requests.post(url,headers=headers)
resp.encoding='utf-8'
photo_list=re.findall(r'"headPhotoUrl":"(.+?)",',resp.text)

age_list=re.findall(r'"age":(.+?),',resp.text)
user_list=re.findall(r'"userID":(.+?),',resp.text)
nick_list=re.findall(r'"nickname":(.+?),',resp.text)
#这个是正则表达式 找nickname的 直到‘，’为止
print(photo_list)
with open("templates/userID.txt", "w", encoding="utf-8") as f:
    for i,u in zip(photo_list,user_list):
        img_url='http:'+i.replace('\\','')
        urlretrieve(img_url,f'./templates/壁纸/{u}.jpg')
    # print(age_list)
    # print(nick_list)
        f.write(f'userID:{u}\n')
