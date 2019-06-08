from django.shortcuts import render
from django.views.generic import FormView, ListView

from .models import Images
from .forms import UploadFormImage, UploadFormURL
from .file_manager import file_manager_requests

from datetime import datetime
import hashlib
from PIL import Image
import os
import math


def get_upload_page(request):
    return render(request, 'upload.html')


def clear_dir():
    if os.listdir('media/img/resized/'):
        for file in os.listdir('media/img/resized/'):
            os.remove('media/img/resized/' + file)


def get_image(request, img):
    clear_dir()

    image = Images.objects.get(img=f'img/{img}')
    if request.GET:
        new_image = Image.open(f'media/{image.img}')

        new_image = new_image.resize((int(request.GET.get('width')) if request.GET.get('width') else new_image.size[0],
                                      int(request.GET.get('height')) if request.GET.get('height') else new_image.size[1]),
                                     Image.ANTIALIAS)
        new_image_path = f'media/img/resized/{hashlib.md5(str(datetime.today()).encode()).hexdigest() + "-" + img}'
        new_image.save(new_image_path)

        new_image_size = os.stat(new_image_path).st_size

        if request.GET.get('size') and int(request.GET.get('size')) < new_image_size:
            image_size = int(math.sqrt(int(request.GET.get('size')))) * 2
            os.remove(new_image_path)
            new_image = new_image.resize((image_size, image_size), Image.ANTIALIAS)
            new_image.save(new_image_path)
        return render(request, 'image.html', context={'image_path': '/' + new_image_path})

    return render(request, 'image.html', context={'image_path': '/media/' + str(image.img)})


class IndexView(ListView):
    model = Images
    template_name = 'index.html'
    context_object_name = "links"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['len_links'] = len(Images.get_all_objects())

        return context


class UploadViewImage(FormView):
    form_class = UploadFormImage
    template_name = 'upload_image.html'

    def post(self, request, *args, **kwargs):

        form = UploadFormImage(request.POST, request.FILES)

        if form.is_valid():
            image_obj = Images(
                title=str(request.FILES['image']) + '-' + hashlib.md5(str(request.FILES["image"]).encode() + str(datetime.today()).encode()).hexdigest(),
                img=request.FILES['image']
            )
            image_obj.save()
            return render(request, 'success.html')

        return super(UploadViewImage, self).post(request)


class UploadViewUrl(FormView):
    form_class = UploadFormURL
    template_name = 'upload_url.html'

    def post(self, request, *args, **kwargs):

        form = UploadFormURL(request.POST)

        if form.is_valid():
            response = file_manager_requests(request.POST['url'])
            '''date_and_type = file_manager(request)

            if date_and_type:
                new_object = Images(title=date_and_type[0], img=f'img/{date_and_type[0]}.{date_and_type[1]}')
                new_object.save()'''
            if response:
                return render(request, 'success.html')

            return render(request, 'error.html')

        return super(UploadViewUrl, self).post(request)
