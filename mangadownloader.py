#-*- coding: utf-8 -*-

# (c) 2013-2014 Squizduos Labs LLC. All rights reserved.
# This code is licensed under the GNU General Public License, version 2 or later.

# (c) 2013-2014 Семён Бочкарёв. Все права защищены.
# Данный код распространяется на условиях лицензии GNU GPL версии 2 или более поздней

import lxml.html
import urllib.request
import codecs
import logging
import os

class Chapter:
    # Класс, который обозначает главу манги
    def __init__(self, link, vol_number, ch_number):
        self.link = link
        self.vol_number = vol_number
        self.ch_number = ch_number


class MangaDownloader:
    def get_chapters_list(link):
        # Данная процедура скачивает список глав манги, ссылка на которую передаётся в качестве единственного параметра
        my_request = urllib.request.Request(link)
        # Данные заголовки необходимы, чтобы сайт считал нас браузером
        my_request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0)\
                                            Gecko/20100101 Firefox/24.0')
        try:
            page = urllib.request.urlopen(my_request)
        except:
            # Ошибка сети
            return 1
        text = page.read().decode(encoding='UTF-8')
        doc = lxml.html.document_fromstring(str(text))
        links = []
        # Ищем главы манги
        for element in doc.cssselect("html body div#mangaBox.pageBlock div.leftContent div.expandable"):
            for chapter in element.cssselect("tr td a"):
                if chapter.attrib['href'].startswith('/'):
                    links.append(chapter.attrib['href'])
        if len(links) == 0:
            return 2
        return links

    def download_chapters(link, path):
        # Данная процедура скачивает в данную папку главу манги
        my_request = urllib.request.Request(link)
        # Данные заголовки необходимы, чтобы сайт считал нас браузером
        my_request.add_header('User-Agent', "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0)\
                                            Gecko/20100101 Firefox/24.0")
        try:
            page = urllib.request.urlopen(my_request)
        except:
            return 1
        text = page.read().decode(encoding="UTF-8")
        doc = lxml.html.document_fromstring(str(text))
        # Ищем ссылки на данное изображение
        for element in doc.xpath("/html/body/div[4]/script"):
            if element.text.find('pictures') != -1:
                script_text = element.text
        try:
            script_lines = script_text.split("\n")
        except:
            #Если не существует, то глав не найдено-с
            return 3
        for line in script_lines:
            if line.find('var pictures') != -1:
                pictures_line = line
        pictures_line = pictures_line.split('=')[1]
        links = []
        #Устанавливаем левую и правую границы поиска
        n1 = 0
        n2 = 0
        while (n1 != -1 and n2 != -1):
            n1 = pictures_line.find("url:", n2)
            n2 = pictures_line.find(",w:", n1)
            if (n1 != -1 and n2 != -1):
                link = pictures_line[n1+5:n2-1]
                links.append(link)
        if len(links) < 1:
            return 4
        for download_link in links:
            filename = download_link.split("/")[-1]
            try:
                image_file = urllib.request.urlretrieve(download_link, os.path.join(path, filename))
            except:
                print('Error while downloading file ' + download_link + ", trying again")
                try:
                    image_file = urllib.request.urlretrieve(download_link, os.path.join(path, filename))
                except:
                    print('Error while downloading file ' + download_link + ", passing...")

            #print(download_link)
            #image = urllib.request.urlopen(download_link)
            #image_file = open(os.path.join(path, filename), 'wb')
            #image_file.write(image.read())
            #image_file.close()
        return 0
