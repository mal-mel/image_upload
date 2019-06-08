from django.contrib import admin
from django.urls import path
from upload.views import IndexView, UploadViewImage, UploadViewUrl, get_upload_page, get_image
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('upload/from_image/', UploadViewImage.as_view()),
    path('upload/from_url/', UploadViewUrl.as_view()),
    path('upload/', get_upload_page),
    path('img/<str:img>/', get_image)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
