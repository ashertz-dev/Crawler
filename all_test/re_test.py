import re


info = "姓名:Hypnos1998 生日:1998年4月16日 本科-2017.09.01"
match_result = re.match(r".*姓名.*?([a-zA-Z]+).*?生日.*?(\d{2,4}).*?本科.*?(\d{2,4})", info)
print(len(match_result.groups()))
print(match_result.group(0))
print(match_result.group(1))
print(match_result.group(2))
print(match_result.group(3))




