import re
str = '<li><a href="/song?id=111111">晴天</a></li><li><a href="/song?id=22222">等你下课</a></li>'
reg1 = r'<li><a href="/song\?id=\d*?">.*</a></li>'
result = re.compile(pattern=reg1).findall(str)
print(result)
