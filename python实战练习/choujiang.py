from flask import Flask,render_template
from random import randint
app=Flask(__name__)
hero = [
    '黑暗之女', '狂战士', '正义巨像', '卡牌大师', '德邦总管', '无畏战车', '诡术妖姬',
    '猩红收割者', '远古恐惧', '正义天使', '无极剑圣', '牛头酋长', '符文法师', '亡灵战神', '战争女神'
]
@app.route('/choujiang')
def choujiang():
    num=randint(1,len(hero)-1)
    return render_template("index.html",hero=hero,h=hero[num])
app.run(debug=True)