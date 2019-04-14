import os
from datetime import datetime

TYPES = ['.jpg', '.jpeg', '.gif', '.png', 'tiff', 'psd', '.bmp']


def file_manager(request):

    date = str(datetime.today()).replace(' ', '_')[:-7]

    for format_img in TYPES:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        print(os.getcwd())
        if format_img in request.POST['url']:

            os.system(f"wget -O {os.getcwd()}/media/img/{date} {request.POST['url']}")

            type_of_file = \
            os.popen(f'file {os.getcwd()}/media/img/{date}').read().split(' ')[1].lower()

            os.system(
                f'mv {os.getcwd()}/media/img/{date}'
                f' {os.getcwd()}/media/img/{date}.{type_of_file}')

            return date, type_of_file

    return False

