import os
import sys
from flask import Flask, render_template
import click
# from flask import url_for
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


class User(db.Model):  # 表名会是user (自动生成。小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名会是movie
    id = db.Column(db.Integer, primary_key=type)  #主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))    # 电影年份


# 自定义命令 initdb
@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:    # 判断是否出入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized databases.')  # 输出提示信息


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

