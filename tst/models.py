from django.db import models
from django import forms

class upload(models.Model):
    name = models.CharField(max_length=200 ,default="",unique=True)
    video = models.FileField(upload_to='static/',default="",)
    
class uf(forms.ModelForm):
    class Meta:
        model = upload
        fields = "__all__"