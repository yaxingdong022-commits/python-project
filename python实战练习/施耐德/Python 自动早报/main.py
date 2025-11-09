# main.py
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import os
from config import *

# ==================== 1. 获取数据 ====================
def get_weather():
    try:
        url = f"http://wttr.in/{CITY}?format=%C+%t"
        r = requests.get(url, timeout=5)
        return r.text.strip()
    except:
        return "晴，适合写代码"

def get_news():
    # 免费新闻API（每日热点）
    try:
        url = "https://api.qq.com/v1/news"
        r = requests.get("https://v1.hitokoto.cn/")
        data = r.json()
        return data.get('hitokoto', '今天也要加油！')
    except:
        return "今天也要加油哦~"

# ==================== 2. 生成早报图片 ====================
def create_report_image():
    width, height = 600, 400
    img = Image.new('RGB', (width, height), color='#f0f8ff')
    draw = ImageDraw.Draw(img)

    # 尝试加载中文字体（没有就用默认）
    try:
        font_title = ImageFont.truetype("simhei.ttf", 36)
        font_text = ImageFont.truetype("simhei.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # 标题
    today = datetime.now().strftime("%Y年%m月%d日 星期%w")
    draw.text((50, 30), f"早安！{today.replace('星期0', '日').replace('星期', '')}", fill='black', font=font_title)

    # 内容
    weather = get_weather()
    news = get_news()
    draw.text((50, 120), f"天气：{weather}", fill='#0066cc', font=font_text)
    draw.text((50, 180), f"鸡汤：{news}", fill='#cc3300', font=font_text)
    draw.text((50, 240), "今天也要元气满满！", fill='#ff6600', font=font_text)

    # 保存
    img_path = "morning_report.jpg"
    img.save(img_path)
    return img_path

# ==================== 3. 发送邮件 ====================
def send_email(img_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"早报 {datetime.now().strftime('%Y-%m-%d')}"

    text = MIMEText("你的专属早报来啦！", 'plain', 'utf-8')
    msg.attach(text)

    with open(img_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<image1>')
        msg.attach(img)

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败：", e)

# ==================== 4. 微信推送（可选）================
def send_wechat():
    if not SENDKEY:
        return
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    data = {
        "title": "早报来啦！",
        "desp": f"{get_weather()}\n\n{get_news()}"
    }
    requests.post(url, data=data)

# ==================== 5. 主函数 ====================
def job():
    print(f"[{datetime.now()}] 开始生成早报...")
    img_path = create_report_image()
    send_email(img_path)
    send_wechat()
    print("早报发送完成！")

# ==================== 6. 启动定时任务 ====================
if __name__ == "__main__":
    # 每天 7:00 执行
    schedule.every().day.at("07:00").do(job)

    # 测试：立即运行一次
    print("正在测试发送...")
    job()

    print("早报系统已启动，每天7点自动推送...")
    while True:
        schedule.run_pending()
        time.sleep(60)