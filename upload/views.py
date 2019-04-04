from django.shortcuts import render
from django.views.generic import FormView, TemplateView, ListView
from .models import Images
from .forms import UploadFormImage, UploadFormURL
from .file_manager import file_manager
from datetime import datetime


def get_upload_page(request):
    return render(request, 'upload.html')


class IndexView(ListView):
    model = Images
    template_name = 'index.html'
    context_object_name = "links"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['len_links'] = len(Images.get_all_objects()) - 1

        return context


class UploadViewImage(FormView):
    form_class = UploadFormImage
    template_name = 'upload_image.html'

    def post(self, request, *args, **kwargs):

        form = UploadFormImage(request.POST, request.FILES)

        if form.is_valid():
            new_object = Images(title=str(datetime.today()).replace(' ', '_')[:-7], img=request.FILES["image"])
            new_object.save()
            return render(request, 'success.html')

        return super(UploadViewImage, self).post(request)


class UploadViewUrl(FormView):
    form_class = UploadFormURL
    template_name = 'upload_url.html'

    def post(self, request, *args, **kwargs):

        form = UploadFormURL(request.POST)

        if form.is_valid():
            date_and_type = file_manager(request)

            if date_and_type:
                new_object = Images(title=date_and_type[0], img=f'img/{date_and_type[0]}.{date_and_type[1]}')
                new_object.save()

                return render(request, 'success.html')

            return render(request, 'error.html')

        return super(UploadViewUrl, self).post(request)
