from django import forms

class ImageUploadForm(forms.Form):

    """Image upload form."""

    name = forms.CharField()
    architect = forms.CharField()
    image = forms.ImageField()