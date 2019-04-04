from django import forms


class UploadFormImage(forms.Form):
    image = forms.ImageField(required=True)


class UploadFormURL(forms.Form):
    url = forms.URLField(required=True)
