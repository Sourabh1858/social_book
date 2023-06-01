from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _




class BloggerManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_blogger(self, email, password,username,  **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        # email = self.normalize_email(email)
        # publicVisibility = True
        blogger = self.model(email=email,username=username, password=password, **extra_fields)
        

        # blogger.set_password(password)

        blogger.save()
        return blogger
    

class LikesManager(BaseUserManager):
    def create_Likes(self,blog_id,count,  **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        print("Inside LikesManager")
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        # email = self.normalize_email(email)
        # publicVisibility = True
        likes = self.model(blog_id=blog_id,count=count, **extra_fields)
        

        # blogger.set_password(password)

        likes.save()
        return likes

class CommentsManager(BaseUserManager):
    def create_comments(self, blog,comments,username,  **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        # email = self.normalize_email(email)
        # publicVisibility = True
        print("blog value in manager.py",blog)
        comments = self.model(blog_id=blog.id,comments=comments,username=username, **extra_fields)
        

        # blogger.set_password(password)

        comments.save()
        return comments


   