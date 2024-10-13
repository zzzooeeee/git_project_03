import requests
from bs4 import BeautifulSoup
import pymysql.cursors

from spider01.test02 import proxies

stars=0
for i in range(1,11):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 database='spider_douban',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    # proxies={"http":"136.226.194.151:9480"}

    r = requests.get('https://movie.douban.com/top250', headers=headers)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all("div", class_='item')
    with connection:
        for item in items:
            img = item.find("div", class_="pic").a.img  # 寻找img标签
            name = img['alt']
            url = img['src']

            hd = item.find("div", class_="hd")
            English = hd.find_all("span")
            Englishname = English[1].text  # 英文名称
            Othername = hd.find("span", class_="other").text  # 台式名称

            bd = item.find("div", class_="bd")
            director = item.find("div", class_="bd").p.text.strip()  # 导演，演员简介

            star = bd.find("div", class_="star")
            level = star.find("span", class_="rating_num").text  # 豆瓣评分
            comments = star.find_all("span")
            comment = comments[3].text  # 评价人数
            label = bd.find("span", class_="inq")  # 标签
            # 处理my_object为None的情况
            if label is not None:
                label = bd.find("span", class_="inq").text
            else:
                label = bd.find("span", class_="inq")

            with connection.cursor() as cursor:
                sql = "INSERT IGNORE `movie_info` (`movie_name`,`movie_url`,`englishname`,`othername`,`director`,`level`,`comment`,`label`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (name, url, Englishname, Othername, director, level, comment, label))
        connection.commit()
    stars = stars + 1
