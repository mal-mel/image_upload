import os
from datetime import datetime
import httplib2
import hashlib

from .models import Images

TYPES = ['.jpg', '.jpeg', '.gif', '.png', '.tiff', '.psd', '.bmp']


def file_manager(request):  # Скачивание изображения через bash

    date = str(datetime.today()).replace(' ', '-')[:-7]

    for format_img in TYPES:

        if format_img in request.POST['url']:

            os.system(f"wget -O {os.getcwd()}/media/img/{date} {request.POST['url']}")

            type_of_file = \
            os.popen(f'file {os.getcwd()}/media/img/{date}').read().split(' ')[1].lower()

            os.system(
                f'mv {os.getcwd()}/media/img/{date}'
                f' {os.getcwd()}/media/img/{date}.{type_of_file}')

            return date, type_of_file

    return False


def file_manager_requests(url):  # Скачивание изображения через httplib
    date = str(datetime.today()).replace(' ', '-')[:-7]

    h = httplib2.Http('.cache')
    response, content = h.request(url)

    for img_format in TYPES:
        if img_format in url:
            with open(f'{os.getcwd()}/media/img/{date}{img_format}', 'wb') as image:
                image.write(content)
                image.close()
                Images.objects.create(title=hashlib.md5(str(datetime.today()).encode()).hexdigest(),
                                      img=f'img/{date}{img_format}')
                return True  # В случае если в url есть формат файла из списка форматов
    return False

