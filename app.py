import os
import sys

import click
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from werkzeug.security import generate_password_hash, check_password_hash

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(
    app.root_path, 'data.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于app.secret_key='dev' 设置cookie 签名所需密钥
db = SQLAlchemy(app)  # 初始化扩展 ，传入程序实例
login_manager = LoginManager(app)  # 实例化扩展
login_manager.login_view = 'login'  # 设置登录视图端点'login' 为跳转的页面 url


class User(db.Model, UserMixin):  # 表名会是user (自动生成。小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接收密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):  # 表名会是movie
    id = db.Column(db.Integer, primary_key=type)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# 自定义命令 initdb
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否出入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized databases.')  # 输出提示信息


# 生成虚拟数据
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
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
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()


@app.cli.command()
@click.option('--username', prompt=True, help='The username userd to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')
def admin(username, password):
    '''Create user'''
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user ... ')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user ...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()  # 提交数据回话
    click.echo('Done.')


'''
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
'''


# 模版上下文处理函数  对于多个模版内都需要使用的变量 使用app.context_processor 装饰器注册一个模版上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {'user':user}


'''
这个函数返回的变量将会统一注入到每一个模版中的上下文环境中，因此可以直接在模版中使用
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是POST请求
        if not current_user.is_authenticated:  # 如果当前用户为认证
            return redirect(url_for('index'))  # 重定向到主页
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的name值
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示 错误提示
            return redirect(url_for('index'))  # 重定向回主页
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据回话
        db.session.commit()  # 提交数据回话
        flash('Item created')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回首页
    # user = User.query.first()
    movies = Movie.query.all()
    # return render_template('index_bak.html', user=user, movies=movies)
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库回话
        flash('Item updated')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受POST请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接收异常对象作为参数
    # user = User.query.first()
    # return render_template('404.html', user=user), 404  # 返回模版和状态码
    return render_template('404.html'), 404  # 返回模版和状态码


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    user = User.query.get(int(user_id))  # 用户ID为User模型的主键查询对应的用户
    return user  # 返回用户对象


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))
        flash('Invalid username or password.')  # 如果验证失败，显示错误信息
        return redirect(url_for('login'))  # 重定向回登录页面
    return render_template('login.html')


@app.route('/logout')
@login_required  # 用户视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象 # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Setting updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')


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
