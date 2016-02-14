#-*- coding: utf-8 -*-

# (c) 2013-2014 Squizduos Labs LLC. 
# This code is licensed under the GNU General Public License, version 2 or later.

# (c) 2013-2014 Семён Бочкарёв. 
# Данный код распространяется на условиях лицензии GNU GPL версии 2 или более поздней

import mangadownloader as md
import urllib
import os
from multiprocessing.dummy import Pool as WorkerPool


# Вводим ссылку на сайт

print("Введите ссылку на мангу с сайта readmanga.me или mintmanga.com")

link = input()
link_components = urllib.parse.urlparse(link)

if (link_components.netloc == 'readmanga.me' or
    link_components.netloc == 'adultmanga.ru' or
    link_components.netloc == 'mintmanga.com'):
        
    pathCount = link_components.path[1:].count('/') #обработка адреса
    if pathCount != 0:
        first = link_components.path[1:].find('/')
        manga_name = link_components.path[1:first+1]
    else:
        manga_name = link_components.path[1:]
        
    chapters = md.MangaDownloader.get_chapters_list('http://'+link_components.netloc+'/'+manga_name)
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
              chapters_to_download_list = list(map(int, input_string.split()))
        download_all = False
        if len(chapters_to_download_list) == 0:
            download_all = True
        work_directory = os.curdir
        if not os.path.exists(os.path.join(work_directory, manga_name)):
            os.mkdir(os.path.join(work_directory, manga_name))
        pool = WorkerPool(len(chapters_list)) #лимита на закачку нет
        for chapter in chapters_list:
            if (ch != -1):
                if (download_all == True) or (chapter['ch'] in chapters_to_download_list):
                    vol_path = os.path.join(work_directory, manga_name, str(chapter['vol']).zfill(4))
                    if not os.path.exists(vol_path):
                        os.mkdir(vol_path)
                    ch_path = os.path.join(work_directory, manga_name, str(chapter['vol']).zfill(4), str(chapter['ch']).zfill(4))
                    if not os.path.exists(ch_path):
                        os.mkdir(ch_path)
                    #Download manga to directory
                    
                    pool.apply_async(md.MangaDownloader.download_chapters,('http://'+link_components.netloc+chapter['link'], ch_path))
                    
        lastProgress = 0
        while md.progress < md.pages or md.pages == 0:
            if lastProgress != md.progress:
                print("\rloaded " + str(md.progress) + "/" + str(md.pages), end="")
                lastProgress = md.progress
        print("\ndownload complete")
        pool.close()
        pool.join()

