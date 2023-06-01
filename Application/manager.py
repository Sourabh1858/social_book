from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _




class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password,username, publicVisibility, address, birthYear,age, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        # publicVisibility = True
        user = self.model(email=email,username=username,  publicVisibility=publicVisibility, address=address, birthYear=birthYear,age=age, **extra_fields)
        

        user.set_password(password)

        user.save()
        return user


    def create_superuser(self, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        # return self.create_user(email, password, **extra_fields)
        # return self.create_user(self, email, password,username, publicVisibility=True, address="pune", birthYear=1997,age=0, **extra_fields)
        
        # if not email:
        #     raise ValueError(_("The Email must be set"))
        
        # # user.set_username("super")
        # # publicVisibility = True
        # email=self.normalize_email(email)
        user = self.model( **extra_fields)
        user.set_password(password)
        
        

        user.save()
        return user