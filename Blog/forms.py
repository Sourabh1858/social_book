from django import forms
from .models import UploadedBlogs

class UploadBlogForm(forms.ModelForm):
    class Meta:
        model = UploadedBlogs
        fields = ['user','title', 'description',  'image','time']

        # widgets= {
        #     'user': forms.HiddenInput(),
        #  }

 