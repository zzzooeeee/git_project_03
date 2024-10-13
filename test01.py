import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors

start = 0
for i in range(1,11):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='spider_douban',
        cursorclass=pymysql.cursors.DictCursor
    )

    # 创建一个Request(等于一个url),Request需要放在headers
    h = {
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36 (KHTML,like Gecko)Chrome/124.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(f"https://movie.douban.com/top250?start={start}&filter=", headers=h)

    # 参数可以是一个url地址，也可以是一个Request
    r = urllib.request.urlopen(req)
    # print(r.status)
    # print(r.read().decode())

    html_doc = r.read().decode()

    # 使用bs4或者是re正则表达式进行数据提取
    soup = BeautifulSoup(html_doc, 'html.parser')

    items = soup.find_all("div", class_="item")

    # print(items)
    with connection:
        for item in items:
            img = item.find("div", class_="pic").a.img
            name = img['alt']
            url = img['src']
            title = item.find_all("span")
            title_english = title[1].text
            other = item.find("span", class_="other").text
            dictor = item.find("div", class_="bd").p.text
            score = item.find("span", class_="rating_num").text
            star = item.find("div", class_="star")
            comments = star.find_all("span")
            comment = comments[3].text
            bd = item.find("div", class_="bd")
            summary = bd.find("span", class_="inq")
            if summary is not None:
                summary = bd.find("span", class_="inq").text
            else:
                summary = None

            # 把数据提取后，存储到MySQL
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `movie_info1` (`title`,`src`,`title_english`,`other`,`dictor`,`score`,`comment`,`summary`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (name, url, title_english, other, dictor, score, comment, summary))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    start = start + 25





