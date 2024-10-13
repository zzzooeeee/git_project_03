import urllib.request


h = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36 (KHTML,like Gecko)Chrome/124.0.0.0 Safari/537.36"
    }


req = urllib.request.Request("http://httpbin.org/get", headers=h)


# r = urllib.request.urlopen(req)
property_handler=urllib.request.ProxyHandler
opener=urllib.request.build_opener(property_handler)
r=opener.open(req)


print(r.status)
print(r.msg)
print(r.read().decode())








