from peewee import *


db = MySQLDatabase("spider", host="127.0.0.1", port=3306, user="root", password="zz0416..")


class BaseModel(Model):
    class Meta:
        database = db


class Topic(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField()
    content = TextField(default="")
    author = CharField()
    create_time = DateTimeField()
    answer_nums = IntegerField(default=0)
    click_nums = IntegerField(default=0)
    # 点赞数
    praised_nums = IntegerField(default=0)
    # 结帖率
    jtl = FloatField(default=0.0)
    # 赏分
    score = IntegerField(default=0)
    # 状态
    status = CharField()
    last_answer_time = DateTimeField()


class Answer(BaseModel):
    topic_id = IntegerField()
    author = CharField()
    content = TextField(default="")
    create_time = DateTimeField()
    praised_nums = IntegerField(default=0)


class Author(BaseModel):
    id = CharField(primary_key=True, max_length=190)
    name = CharField()
    # 原创数
    original_nums = IntegerField(default=0)
    # 排名
    rate = CharField(default="0")
    desc = TextField(null=True)
    job = CharField(null=True)
    # 粉丝数
    fans = IntegerField(default=0)
    # 关注数
    followers = IntegerField(default=0)



if __name__ == '__main__':
    db.create_tables([Topic, Answer, Author])
