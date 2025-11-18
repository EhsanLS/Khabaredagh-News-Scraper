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
        file.write(
            "<head>\n<meta charset='UTF-8'>\n<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n<title>News</title>\n<link rel='stylesheet' href='../css_directory/style1.css'>\n</head>\n")
        file.write("<body>\n")
        file.write('<header>\n<div class="header-nav-bar">\n')
        if previous_page_title:
            file.write(
                f"<a href='./{previous_page}'>{previous_page_title}</a>\n")
        file.write("<a href='./index.html'>صفحه اصلی</a>\n")
        if next_page_title:
            file.write(
                f"<a href='./{next_page}'>{next_page_title}</a>\n")
        file.write("</div>\n")

        file.write(f"<h1>{fa_section_name}</h1>\n</header>\n")
        file.write("<div id='content'>\n")

        for index in range(len(section_news_list)):
            title = section_news_list[index]
            link = section_links_list[index]
            if len(title) > 100:
                title = title[:100] + " ..."

            file.write(f"<a href='{base_url}{link}'>{title}</a>\n")

        file.write("</div>\n")

        file.write("<div class='footer-nav-bar'>\n")
        if previous_page_title:
            file.write(
                f"<a href='./{previous_page}'>{previous_page_title}</a>\n")
        file.write("<a href='./index.html'>صفحه اصلی</a>\n")
        if next_page_title:
            file.write(
                f"<a href='./{next_page}'>{next_page_title}</a>\n")

        file.write("</div>\n")
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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News</title>
    <link rel="stylesheet" href="../css_directory/style.css">
</head>
<body>
    <div>
        <a href='sport.html'><b>ورزشی</b></a>
        <a href='political.html'><b>سیاسی</b></a>
        <a href='health.html'><b>سلامتی</b></a>
        <a href='art-and-culture.html'><b>فرهنگ و هنر</b></a>
        <a href='science-and-technology.html'><b>علم و فناوری</b></a>
    </div>
</body>
</html>
''')

full_path = os.path.abspath('./html_directory/index.html')
url = f'file://{full_path}'
webbrowser.open(url)
