import requests
from flask import request, render_template,Flask
from flask_cors import CORS
app = Flask(__name__)
@app.route("/")
def index():
    return render_template('Show.html')

@app.route('/ChaXun')
def ChaXun():
    name=request.args.get('name')
    age=request.args.get('age')
    gender=request.args.get('gender')
    hobby=request.args.get('hobby')
    return f'您好！{name}<br>年龄：{age}<br>性别：{gender}<br>爱好：{hobby}'
app.run(debug=True)