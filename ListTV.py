from typing import List, Any

import requests
import zipfile
import re
from datetime import datetime

zalaChanels = ['Первый канал',
               'Беларусь 1',
               'Беларусь 2',
               'Беларусь 3',
               'Беларусь 5',
               'СТВ',
               'МИР',
               'РТР Беларусь',
               'НТВ Беларусь',
               'ТНТ',
               'ВТВ (Первый музыкальный)',
               'ТВ-3',
               'Киномикс',
               'TV1000',
               'Любимое кино',
               'Мужское кино',
               'Русский Иллюзион',
               'TV1000 Русское кино',
               'Еврокино',
               'Viasat History',
               'History',
               'Viasat Explorer',
               'Наш Футбол HD',
               'Иллюзион +',
               'Наше Новое Кино',
               'Кинохит',
               'TV1000 Action',
               'Сарафан ТВ',
               'Настоящее Страшное ТВ',
               'Ностальгия',
               'Киносемья',
               'Кинопремьера',
               'Родное кино']

dayOfWeek = ['ПОНЕДЕЛЬНИК',
             'ВТОРНИК',
             'СРЕДА',
             'ЧЕТВЕРГ',
             'ПЯТНИЦА',
             'СУББОТА',
             'ВОСКРЕСЕНЬЕ']

monthDict = {'Январь': 1,
             'Февраль': 2,
             'Март': 3,
             'Апрель': 4,
             'Май': 5,
             'Июнь': 6,
             'Июль': 7,
             'Август': 8,
             'Сентябрь': 9,
             'Октябрь': 10,
             'Ноябрь': 11,
             'Декабрь': 12}

listtvZipFileName = 'inter-tv.zip'
listtvFileName = 'inter-tv.txt'
workPath = "D:\\SRC\\ListTV\\"
zipUrl = 'https://www.teleguide.info/download/new3/inter-tv.zip'
'''
f = open(workPath + listtvZipFileName, "wb")  # открываем файл для записи, в режиме wb
ufr = requests.get(zipUrl)  # делаем запрос
f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
f.close()

with zipfile.ZipFile(workPath + listtvZipFileName) as zf:
    try:
        info = zf.getinfo(listtvFileName)
    except KeyError:
        print('ERROR: Did not find {} in zip file'.format(
            listtvFileName))
    else:
        print('{} is {} bytes'.format(
            info.filename, info.file_size))
        zf.extract(listtvFileName, workPath)
'''
chanels = []
prHour = 0
prMinute = 0
prDay = 1
prMonth = 1
prYear = datetime.now().year

currentChanel = 'other'
needPrNext = False
skipNext = False
inProg = False
inPer = False
per = ''
needPrint = True
goodChanel = 0

with open(listtvFileName, 'r') as f:
    for line in f:
        if goodChanel > 0:
            if goodChanel == 1:
                goodChanel += 1
                continue
            else:
                if line[0] == '\n':
                    goodChanel = 0
                    continue
                else:
                    # print(line.strip('\n'))
                    result = re.findall(r'^\d\d:\d\d+', line)
                    if len(result) != 0:  # старая передача закончилась, надо начать новую
                        prHour = int(result[0][:2])
                        prMinute = int(result[0][3:5])

                        print('{}-{}-{} {}:{} {}'.format(prDay, prMonth, prYear, prHour, prMinute, per))
                        per = line[6:].strip('\n')
                    else:
                        per += line[6:].strip('\n')
                    continue
        for dow in dayOfWeek:
            match = re.match(dow, line)
            if match:  # обнаружен заголовок программы на день определенного канала
                result = re.split(r'\.\s', line.strip('\n'))
                currentChanel = result[2]  # наименование канала
                result2 = re.split(r'\s', result[1])  # извлечь дату программы ['7','Октябрь']
                prDay = int(result2[0])
                prMonth = monthDict[result2[1]]
                if currentChanel in zalaChanels:
                    goodChanel = 1
                    print(line.strip('\n'))
                break

