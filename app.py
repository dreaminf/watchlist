import os
import sys
from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(
    app.root_path, 'data.db'
)
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)  # 初始化扩展 ，传入程序实例

name = 'Zhenghl'
# 列表
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1984'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1986'},
    {'title': 'Leon', 'year': '1987'},
    {'title': 'Mahjong', 'year': '1998'},
    {'title': 'Swallowtail Butterfly', 'year': '1980'},
    {'title': 'King of Comedy', 'year': '1986'},
    {'title': 'Devils on the Doorstep', 'year': '1988'},
    {'title': 'WALL-E', 'year': '1981'},
    {'title': 'The Pork of Music', 'year': '1984'},
]


@app.route('/')
def index():
    return render_template('index.html', name=name,
                           movies=movies)


'''
@app.route('/user/<names>')
def user_page(names):
    return 'User :%s' % names


# test page
@app.route('/test')
def test_url_for():

    print(url_for('index'))
    print(url_for('user_page', name='zhl'))
    print(url_for('user_page', name='zyl'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))

    return 'Test page'
'''

