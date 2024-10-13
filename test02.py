import urllib.request

from urllib.request import ProxyHandler

h = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

req = urllib.request.Request("http://httpbin.org/get",headers=h)

# proxies = {"http":"112.17.10.41:3128"}

proxies={"http":"127.0.0.1:7890"}

proxy_handler = urllib.request.ProxyHandler(proxies=proxies)
opener=urllib.request.build_opener(proxy_handler)

r = opener.open(req)



# r=urllib.request.urlopen("http://www.sohu.com/")
# print(r.status)
# print(r.msg)
print(r.read().decode())
