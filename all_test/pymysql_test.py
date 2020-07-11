import pymysql


conn = pymysql.connect(host="localhost",
                       user="root",
                       password="zz0416..",
                       db="test",
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        sql = """create table if not exists `test_table`(
        `id` int not null auto_increment,
        `title` varchar(50) not null ,
        `text` varchar(500) not null,
        primary key (`id`))"""
        cursor.execute(sql)
        conn.commit()
except Exception as e:
    print(e)
    print("false")
print("This is a test")
