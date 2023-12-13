# -*- coding:utf-8-sig -*-
from flask import Flask, render_template, request, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from config import USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE
from crawler import url_response
from message import get_message
from transformers import AutoModel, AutoTokenizer
from database import create_table, insert_data, load_data
import json
# 这里是模型的启动加载
tokenizer = AutoTokenizer.from_pretrained("E:\ChatGLM\ChatGLM3-main\model\chatglm3-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("E:\ChatGLM\ChatGLM3-main\model\chatglm3-6b", trust_remote_code=True).quantize(4).cuda()
model = model.eval()
history = []
past_key_values = None
# 基础配置
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
db = SQLAlchemy(app)
app.secret_key = '123456'
response_json = []
create_table()


class Page(db.Model):
    __tablename__ = "page"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_url = db.Column(db.String(500), nullable=False)
    page_main_contain = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()
    for key, value in url_response.items():
        temp_page = Page.query.filter_by(page_url=key)
        test_page = temp_page.first()
        temp_json = ''
        if temp_page.count() == 0:
            temp_query, history = model.chat(tokenizer, value, history=[])
            try:
                temp_json = json.loads(temp_query)
            except json.decoder.JSONDecodeError:
                temp_query, history = model.chat(tokenizer, '下面的json数据格式有误请修复并返回正确的格式的json数据:'+temp_query, history=[])
            if len(temp_query) <= 300:
                temp_json['link'] = page.page_url
                page = Page(page_url=key, page_main_contain=str(temp_query))
                db.session.add(page)
                db.session.commit()
            else:
                page = Page(page_url=key, page_main_contain="length_error")
                db.session.add(page)
                db.session.commit()
            #response_json.append(temp_json)
        else:
            for page in temp_page:
                if page.page_main_contain != 'length_error':
                    temp_json = page.page_main_contain
                    try:
                        temp_json = json.loads(temp_json)
                        temp_json['link'] = page.page_url
                        #response_json.append(temp_json)
                    except json.decoder.JSONDecodeError:
                        print(page.page_main_contain)
        try:
            print(temp_json)
        except Exception as e:
            pass
        if temp_json != '':
            insert_data(temp_json)
    response_json = load_data()


def generate_response(input_text, history_query):
    response, history_query = model.chat(tokenizer, input_text, history=history_query)
    return response

@app.route("/login", methods=("GET", "POST"))
def login():
    session['personal_page_json'] = get_message()
    return render_template('list_2.html', json_data=session['personal_page_json'])

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        user_input = request.form['user_input']
        personal_page_data = session.get('personal_page_json')
        if personal_page_data is None:
            user_input = '对不起, 请先进行登录操作在继续进行查询'
            bot_response = ''
        else:
            data_json = ''
            for item in session['personal_page_json']:
                data_json += str(item)+','
            data_json += '以上是一些我最近的行程安排,现在你需要在我询问你的时候告诉我相关的安排'
            bot_response = generate_response(user_input, [{"role": "user", "content": data_json}])
        return render_template('index_01.html', user_input=user_input, bot_response=bot_response)
    return render_template('index_01.html')


@app.route("/", methods=("GET", "POST"))
def web():
    return render_template('list_01.html',
                           json_data=response_json)  # 前一个json_data是html中的变量名，后一个是引用的python文件中的变量名



if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
