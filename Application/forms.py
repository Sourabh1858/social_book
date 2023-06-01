from django import forms
from django.core.validators import FileExtensionValidator
from .models import UploadedFile
from django import forms
from django.core.validators import FileExtensionValidator
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['user','title', 'description',  'cost', 'year_published', 'file']

        widgets= {
            'user': forms.HiddenInput(),
         }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['file'].validators = [
    #         FileExtensionValidator(allowed_extensions=['pdf',  'jpeg'])
    #     ]


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['file'].validators = [
    #         FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg'])
    #     ]
