from datetime import date
from peewee import *
import logging
import json


db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="zz0416..")


class Spider(Model):
    name = CharField(max_length=20)
    birthday = DateField(null=True)
    age = IntegerField()

    class Meta:
        database = db
        table_name = "user"


def create(name):
    # 创建表格
    db.create_tables([name])


def read_json(_path):
    # 读取数据
    _data = []
    with open("data.json", "r") as f:
        _data = json.load(f)
    return _data


def insert(_data):
    # 插入数据
    for info in _data:
        uncle_bob = Spider(name=info.get("name"),
                           birthday=date(info.get("birthday")[0],
                                         info.get("birthday")[1],
                                         info.get("birthday")[2]),
                           age=info.get("age")
                           )
        uncle_bob.save()


if __name__ == '__main__':
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    path = "data.json"
    # 创建表格
    create(Spider)
    # 读取json文件
    data = read_json(path)
    # 将数据插入表格
    insert(data)
    # 查询数据
    query = Spider.select().where(Spider.name == "Hypnos")
    for user in query:
        print(user.id, user.name, user.birthday, user.age)
        # 修改数据或新增数据
        user.age = 100
        user.save()
        # 删除数据
        user.delete_instance()

