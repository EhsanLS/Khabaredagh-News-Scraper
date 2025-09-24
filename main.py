import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import os


def get_links(section_name):
    url = f'https://khabaredagh.ir/fa/{section_name}'
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    stories = s.find_all('a', attrs={'target': '_blank'})

    section_links = []
    for i in stories:
        section_links.append(i['href'])

    index1 = 0
    while index1 < len(section_links) - 1:
        if 'https' in section_links[index1]:
            section_links.remove(section_links[index1])
        if 'https' not in section_links[index1]:
            index1 += 1

    index2 = 0
    while index2 < len(section_links) - 1:
        if section_links[index2] == section_links[index2 + 1]:
            section_links.remove(section_links[index2])
        if section_links[index2] != section_links[index2 + 1]:
            index2 += 1
    section_links.remove(section_links[len(section_links) - 1])
    section_links.remove(section_links[len(section_links) - 1])

    section_news = []
    for i in stories:
        section_news.append(re.sub(r'\s+', ' ', i.text).strip())

    index = 0
    while index < len(section_news) - 1:
        if section_news[index] == '':
            section_news.remove(section_news[index])
        if section_news[index] != '':
            index += 1
    section_news.remove(section_news[len(section_news) - 1])
    section_news.remove(section_news[len(section_news) - 1])
    return section_links, section_news


def make_page(en_section_name, fa_section_name, next_page_title='', next_page='', previous_page_title='',
              previous_page=''):
    base_url = 'https://khabaredagh.ir'
    section_news_list = get_links(en_section_name)[1]
    section_links_list = get_links(en_section_name)[0]
    with open(f"./html_directory/{en_section_name}.html", "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html lang='fa' dir='rtl'>\n")
        file.write("<head>\n")
        file.write("<meta charset='UTF-8'>\n")
        file.write("<title>News</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")

        file.write(f"<div style='text-align: center;'><h1>{fa_section_name}</h1></div>\n")
        file.write("<table border='1' style='margin: auto;'>\n")

        for index in range(len(section_news_list)):
            title = section_news_list[index]
            link = section_links_list[index]
            if len(title) > 100:
                title = title[:100] + " ..."
            file.write("<tr>\n")
            file.write(f"<td><a href='{base_url}{link}' style='text-decoration: none;'>{title}</a></td>\n")
            file.write("</tr>\n")

        file.write("</table>\n")

        if next_page_title:
            file.write(
                f"<div style='text-align: center;'><br><a href='./{next_page}' style='text-decoration: none;'>{next_page_title}</a></div>\n")
        if previous_page_title:
            file.write(
                f"<div style='text-align: center;'><br><a href='./{previous_page}' style='text-decoration: none;'>{previous_page_title}</a></div>\n")

        file.write("<div style='text-align: center;'><br><a href='./index.html' style='text-decoration: none;'>صفحه اصلی</a></div>\n")
        file.write("</body>\n")
        file.write("</html>\n")
    return f"{en_section_name}.html"


make_page('sport', 'ورزشی', 'صفحه بعد', 'political.html')
make_page('political', 'سیاسی', 'صفحه بعد', 'health.html', 'صفحه قبل', 'sport.html')
make_page('health', 'سلامتی', 'صفحه بعد', 'art-and-culture.html', 'صفحه قبل', 'political.html')
make_page('art-and-culture', 'فرهنگ و هنر', 'صفحه بعد', 'science-and-technology.html', 'صفحه قبل', 'health.html')
make_page('science-and-technology', 'علم و فناوری', 'صفحه قبل', 'art-and-culture.html')

with open("html_directory/index.html", "w", encoding="utf-8") as file:
    file.write('''<!DOCTYPE html>
<html lang='fa' dir='rtl'>
<head>
    <style>.centered-list {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }</style>
    <style>li {
        font-size: 30px;
    }</style>
    <style>a {
        text-decoration: none;
    }</style>
    <title>News</title>
</head>
<body>
<div class='centered-list'>
    <ul>
        <li><a href='sport.html'><b>ورزشی</b></a></li>
        <li><a href='political.html'><b>سیاسی</b></a></li>
        <li><a href='health.html'><b>سلامتی</b></a></li>
        <li><a href='art-and-culture.html'><b>فرهنگ و هنر</b></a></li>
        <li><a href='science-and-technology.html'><b>علم و فناوری</b></a></li>
    </ul>
</div>
</body>
</html>
''')

full_path = os.path.abspath('./html_directory/index.html')
url = f'file://{full_path}'
webbrowser.open(url)
