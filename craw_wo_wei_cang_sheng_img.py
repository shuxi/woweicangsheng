import requests
import re
from bs4 import BeautifulSoup
import time

def downPicture(link,page):
    time.sleep(1)
    ir = requests.get(link)
    print(link)
    if ir.status_code == 200:
        open(r'F:\woweicangsheng\%d.png'%(page),'wb').write(ir.content)
    else:
        print(ir.status_code)
    return page+1

def get_chapter_url_from(catalogue):
    url_host = 'http://www.gufengmh.com'
    wb_data = requests.get(catalogue)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    links = soup.select('#chapter-list-1 > li > a')
    for link in links:
        yield url_host+link.get('href')

def get_img_link_from(chapters):
    url_host = 'http://res.gufengmh.com/'
    for chapter in chapters:
        time.sleep(1)
        wb_data = requests.get(chapter)
        wb_data.encoding='utf-8'
        html = wb_data.text
        chapter = re.search('var chapterPath = \"([\w/]+)\";',html)
        imgs = re.search('var chapterImages = \[(.+)]',html)
        if chapter:
            chapter = chapter.groups()[0]
        if imgs:
            imgs = imgs.groups()[0].split(',')
            for img in imgs:
                yield url_host+chapter+img[1:-1]

if __name__ == '__main__':
    url = 'http://www.gufengmh.com/manhua/woweicangsheng/#chapters'
    chapters = get_chapter_url_from(url)
    img_links = get_img_link_from(chapters)
    page = 1
    for link in img_links:
        page = downPicture(link,page)
