import hashlib

m =hashlib.md5()

str = '245861'
str1 = '74274ab4332fc72babf35e46e715dd85'
m.update(str.encode('utf-8'))
res = m.hexdigest()
print(res == str1)