from flask import Flask,render_template
from flask import url_for
app = Flask(__name__)

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


