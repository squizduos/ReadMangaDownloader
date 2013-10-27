#-*- coding: utf-8 -*-

import lxml.html
import urllib.request
import codecs
import logging
import os

class MangaDownloader:
    def get_chapters_list(link):
        my_request = urllib.request.Request(link)
        my_request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0')
        try:
            page = urllib.request.urlopen(my_request)
        except:
            return 'Network error'
        text = page.read().decode(encoding='UTF-8')
        doc = lxml.html.document_fromstring(str(text))
        links = []
        for element in doc.cssselect("html body div#mangaBox.pageBlock div.leftContent div.expandable"):
            for chapter in element.cssselect("tr td a"):
                if chapter.attrib['href'].startswith('/'):
                    links.append(chapter.attrib['href'])
        if len(links) == 0:
            return 'Parsing error'
        return links

    def download_chapters(link, path):
        my_request = urllib.request.Request(link)
        my_request.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0')
        try:
            page = urllib.request.urlopen(my_request)
        except:
            return 'Network error'
        text = page.read().decode(encoding="UTF-8")
        doc = lxml.html.document_fromstring(str(text))
        for element in doc.xpath("/html/body/div[4]/script"):
            if element.text.find('pictures') != -1:
                script_text = element.text
        try:
            script_lines = script_text.split("\n")
        except:
            #Если не существует, то глав не найдено-с
            return 404
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
        for download_link in links:
            image = urllib.request.urlopen(download_link)
            filename = download_link.split("/")[-1]
            image_file = open(os.path.join(path, filename), 'wb')
            image_file.write(image.read())
            image_file.close()