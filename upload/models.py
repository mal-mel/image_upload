from django.db import models


class Images(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='img')

    @staticmethod
    def get_all_objects():
        return Images.objects.all()
