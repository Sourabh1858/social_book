from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db import models
from .manager import CustomUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20,unique=True, null=False,blank=True,default='super')
    email = models.EmailField(_("email address"), unique=True)
    publicVisibility = models.BooleanField(default=False)
    birthYear = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=200,  null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email','birthYear']


    objects = CustomUserManager()


    def __str__(self):
        return self.email



class UploadedFile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=False)
    # visibility = models.BooleanField(default=True)
    # cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    year_published = models.IntegerField(null=False)
    # file = models.FileField(upload_to='testFiles/pdf')
    file = models.FileField(upload_to='testFiles/pdf',validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpeg'])])
    # file = models.FileField()

class Profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    designation=models.CharField(max_length=50,null=False,blank=False)
    salary=models.IntegerField(null=False,blank=False)
    profile_photo=models.ImageField(upload_to='testFiles/profiles')
    # profile_photo=models.FileField(upload_to='testFiles/profiles')

    class Meta:
        ordering=('-salary',)
    
    def _str_(self):
        return "{0}-{1}".format(self.user.username, self.designation)



#reference(https://www.django-rest-framework.org/api-guide/authentication/)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
