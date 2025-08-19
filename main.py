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


def make_page(en_section_name, fa_section_name, next_page_title='', next_page='', previous_page_title='', previous_page=''):
    base_url = 'https://khabaredagh.ir'
    section_news_list = get_links(en_section_name)[1]
    section_links_list = get_links(en_section_name)[0]
    with open(f"./html_directory/{en_section_name}.html", "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html lang='fa' dir='rtl'>")
        file.write("<head>")
        file.write("<style>a{text-decoration: none;}</style>")
        file.write("<style>.center {margin-left: auto;margin-right: auto;}</style>")
        file.write("<title>"'News'"</title>")
        file.write("</head>")
        file.write("<body>")
        file.write(f"<div style='text-align: center;'><h1> {fa_section_name} </h1></div>")
        file.write("<table class='center' border= '1' style= 'border-collapse: collapse'; >")
        index3 = 0
        while index3 < len(section_news_list) - 1:
            file.write("<tr>")
            file.write("<td>")
            file.write("<br>")
            if len(section_news_list[index3]) >= 100:
                file.write(
                    f"<li><a href='{base_url}{section_links_list[index3]}'>{section_news_list[index3][0:100] + ' ...'}</a></li>")
            else:
                file.write(f"<li><a href='{base_url}{section_links_list[index3]}'>{section_news_list[index3]}</a></li>")
            file.write("</td>")
            file.write("</tr>")
            index3 += 1
        file.write("</table>")
        if next_page_title != '':
            file.write("<br>")
            file.write(f"<div style='text-align: center;'><a href='./{next_page}'>{next_page_title}</a></div>")
            file.write("<br>")
        if previous_page_title != '':
            file.write(f"<div style='text-align: center;'><a href='./{previous_page}'>{previous_page_title}</a></div>")
            file.write("<br>")
        file.write(f"<div style='text-align: center;'><a href='./main.html'>صفحه اصلی</a></div>")
        file.write("<br>")
        file.write("<br>")
        file.write("</body>")
        file.write("</html>")
    return f"{en_section_name}.html"


make_page('sport', 'ورزشی', 'صفحه بعد', 'political.html')
make_page('political', 'سیاسی', 'صفحه بعد', 'health.html', 'صفحه قبل', 'sport.html')
make_page('health', 'سلامتی', 'صفحه بعد', 'art-and-culture.html', 'صفحه قبل', 'political.html')
make_page('art-and-culture', 'فرهنگ و هنر', 'صفحه بعد', 'science-and-technology.html', 'صفحه قبل', 'health.html')
make_page('science-and-technology', 'علم و فناوری', 'صفحه قبل', 'art-and-culture.html')

with open("html_directory/main.html", "w", encoding="utf-8") as file:
    file.write("<!DOCTYPE html>")
    file.write("<html lang='fa' dir='rtl'>")
    file.write("<head>")
    file.write(
        "<style>.centered-list{display: flex;flex-direction: column;"
        "align-items: center;justify-content: center; height: 100vh;}</style>")
    file.write("<style>li{font-size: 30px;}</style>")
    file.write("<style>a{text-decoration: none;}</style>")
    file.write("<title>"'News'"</title>")
    file.write("</head>")
    file.write("<body>")
    file.write(
        "<div class='centered-list'><ul>"
        "<li><a href='sport.html'><b>ورزشی</b></a></li>"
        "<li><a href='political.html'><b>سیاسی</b></a></li>"
        "<li><a href='health.html'><b>سلامتی</b></a></li>"
        "<li><a href='art-and-culture.html'><b>فرهنگ و هنر</b></a></li>"
        "<li><a href='science-and-technology.html'><b>علم و فناوری</b></a></li></ul></div>")
    file.write("</body>")
    file.write("</html>")
full_path = os.path.abspath('./html_directory/main.html')
url = f'file://{full_path}'
webbrowser.open(url)
