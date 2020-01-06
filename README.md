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
