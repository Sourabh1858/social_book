from django.db import models
from .manager import BloggerManager,LikesManager,CommentsManager
# from .models import UploadedBlogs

from django.core.validators import FileExtensionValidator


class Blogger(models.Model):
    username=models.CharField(max_length=50,null=False,blank=False)
    email=models.CharField(max_length=50,null=False,blank=False)
    password=models.SlugField(null=False,blank=False,max_length=30)
    

    objects = BloggerManager()


    def __str__(self):
        return self.username

class UploadedBlogs(models.Model):
    user=models.ForeignKey(Blogger,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='testFiles/Blogs')
    likes=models.ManyToManyField(Blogger,related_name='likes',blank=True)
    time=models.DateTimeField(blank=True,null=True)

def num_likes(self):
    return self.likes.count()

# class Likes(models.Model):
#     # user=models.ForeignKey(Blogger,on_delete=models.CASCADE,null=True)
#     blog=models.ForeignKey(UploadedBlogs,on_delete=models.CASCADE,null=True,related_name=UploadedBlogs)
#     count=models.IntegerField(blank=True,default=0)

#     objects=LikesManager()

class Comments(models.Model):
#    user=models.OneToOneField(Blogger,on_delete=models.CASCADE,null=True)
   blog=models.ForeignKey(UploadedBlogs,on_delete=models.CASCADE,null=True)
   comments=models.TextField(blank=True,null=False) 
   username=models.CharField(max_length=50,null=False,blank=False,default='anonymous')
   
   objects=CommentsManager()

