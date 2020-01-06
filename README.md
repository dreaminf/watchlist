# watchlist
## 练习项目 入门 flask web

## 管理环境变量
###pip install python-dotenv
.env .flaskenv  文件中写环境变量

## 模版
### jinjn2 模版渲染引擎

# 自动生成虚拟数据 使用Faker https://github.com/joke2k/faker

#### 扩展Bootstrap-Flask 简化在Flask项目中使用Bootstrap4的步骤
其他css样式： Semantic_UI. Foundation

#使用 SQLAlchemy 操作数据库
```python
pip install flask-sqlalchemy
```
SQLAlchemy——一个 Python 数据库工具 （ORM，即对象关系映射）。借助 SQLAlchemy，你可以通过定义 Python 类来表 示数据库里的一张表（类属性表示表中的字段 / 列），通过对这个类进行各种操作 来代替写 SQL 语句。这个类我们称之为模型类，类中的属性我们将称之为字段。
# 配置变量
为了设置 Flask、扩展或是我们程序本身的一些行为，
我们需要设置和定义一些配 置变量。Flask 
提供了一个统一的接口来写入和获取这些配置变 量：
 Flask.config 字典。配置变量的名称必须使用大写，
写入配置的语句一般 会放到扩展类实例化语句之前。

# 模型类编写
模型类的编写有一些限制： 
模型类要声明继承 db.Model 。
 每一个类属性（字段）要实例化 db.Column ，
 传入的参数为字段的类型，下 面的表格列出了常用的字段类。
  在 db.Column() 中添加额外的选项（参数）可以对字段进行设置。比 如， primary_key 设置当前字段是否为主键。除此之外，常用的选项还有 nullable （布尔值，是否允许为空值）、 index （布尔值，是否设置索 引）、 unique （布尔值，是否允许重复值）、 default （设置默认值） 等。 常用的字段类型如下表所示： 字段类 说明 db.Integer 整型 db.String (size) 字符串，size 为最大长度，比如 db.String(20) db.Text 长文本 db.DateTime 时间日期，Python datetime 对象 db.Float 浮点数 db.Boolean 布尔值

```python
class User(db.Model):  # 表名会是user (自动生成。小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名会是movie
    id = db.Column(db.Integer, primary_key=type)  #主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))    # 电影年份
```
```python
flask shell
from app import db
db.create_all()
db.drop_all()
```
# flask自定义命令
```python
import click
# 自定义命令 initdb
@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:    # 判断是否出入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized databases.')  # 输出提示信息
```