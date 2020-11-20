# import pymysql
#
#
# conn = pymysql.connect(host="localhost",
#                        user="root",
#                        password="zz0416..",
#                        db="test",
#                        charset="utf8mb4",
#                        cursorclass=pymysql.cursors.DictCursor)
# try:
#     with conn.cursor() as cursor:
#         sql = """create table if not exists `test_table`(
#         `id` int not null auto_increment,
#         `title` varchar(50) not null ,
#         `text` varchar(500) not null,
#         primary key (`id`))"""
#         cursor.execute(sql)
#         conn.commit()
# except Exception as e:
#     print(e)
#     print("false")
import re


def next_bigger(n):
    # your code here
    arr = re.findall(".{1}", str(n))
    max_num = arr[-1]
    for i in range(len(arr) - 1, -1, -1):
        max_num = max(max_num, arr[i])
        if max_num > arr[i]:
            lis = sorted(arr[i::]).copy()
            min_num = list(filter(lambda x: x > arr[i], lis))[0]
            arr[i] = min_num
            lis.remove(min_num)
            arr = arr[:i+1]+sorted(lis)
            return "".join(arr)
    return -1


# 59884848459853
# 59884848483559


print(next_bigger(59884848459853))
