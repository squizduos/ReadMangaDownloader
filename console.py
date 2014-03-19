#-*- coding: utf-8 -*-

# (c) 2013-2014 Squizduos Labs LLC. All rights reserved.
# This code is licensed under the GNU General Public License, version 2 or later.

# (c) 2013-2014 Семён Бочкарёв. Все права защищены.
# Данный код распространяется на условиях лицензии GNU GPL версии 2 или более поздней

import mangadownloader
import urllib
import os

# Вводим ссылку на сайт

print("Введите ссылку на мангу с сайта readmanga.me или adultmanga.ru")

link = input()
link_components = urllib.parse.urlparse(link)

if (link_components.netloc == 'readmanga.me' or link_components.netloc == 'adultmanga.ru') and (link_components.path[1:].find('/') == -1):
    manga_name = link_components.path[1:]
    chapters = mangadownloader.MangaDownloader.get_chapters_list('http://'+link_components.netloc+'/'+manga_name)
    chapters_list = []
    #Getting chapters list
    if chapters == 1 or chapters == 2:
        print('Невозможно скачать мангу в данный момент.')
    else:
        for chapter in chapters:
            words_from_name = chapter.split('/')
            try:
                vol = int(words_from_name[2][3:])
                ch = int(words_from_name[3].split('?')[0])
            except:
                vol = 0
                ch = -1
            chapters_list.append(dict(link = chapter, vol = vol, ch = ch))
        print("Введите номера глав, которые вы хотите скачать, через пробел, если хотите скачать все главы, нажмите ENTER")
        input_string = input()
        if (input_string.find('-') != -1):
            num = input_string.find('-')
            l_num = int(input_string[:num])
            r_num = int(input_string[num+1:])
            chapters_to_download_list = list()
            for a in range(l_num, r_num + 1):
                chapters_to_download_list.append(a)
        else:
              chapters_to_download_list = list(map(int, input().split()))
        download_all = False
        if len(chapters_to_download_list) == 0:
            download_all = True
        work_directory = os.curdir
        if not os.path.exists(os.path.join(work_directory, manga_name)):
            os.mkdir(os.path.join(work_directory, manga_name))
        for chapter in chapters_list:
            if (ch != -1):
                if (download_all == True) or (chapter['ch'] in chapters_to_download_list):
                    vol_path = os.path.join(work_directory, manga_name, 'vol'+str(chapter['vol']))
                    if not os.path.exists(vol_path):
                        os.mkdir(vol_path)
                    ch_path = os.path.join(work_directory, manga_name, 'vol'+str(chapter['vol']), 'ch'+str(chapter['ch']))
                    if not os.path.exists(ch_path):
                        os.mkdir(ch_path)
                    #Download manga to directory
                    print('Скачиваем том ' + str(chapter['vol']) + ", главу " + str(chapter['ch']) + '...')
                    print('http://'+link_components.netloc+'/'+chapter['link'])
                    mangadownloader.MangaDownloader.download_chapters('http://'+link_components.netloc+chapter['link'], ch_path)
        print('Манга загружена')
