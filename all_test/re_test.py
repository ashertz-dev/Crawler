import re


info = "姓名:Hypnos1998 生日:1998年4月16日 本科-2017.09.01 \naa 489456456"
infos = "\naa 489456456"
match_result = re.match(r".*姓名.*?([a-zA-Z]+).*?生日.*?(\d{2,4}).*?本科.*?(\d{2,4})", info)
print(info)
print(len(match_result.groups()))
print(match_result.group(0))
print(match_result.group(1))
print(match_result.group(2))
print(match_result.group(3))

search_result = re.search(r"(.*)", info)
print(search_result.groups())

search_result = re.search(r"aa (\d*)%", infos)
if not search_result:
    search_result = 0
else:
    search_result = search_result.group(1)


print(search_result)



