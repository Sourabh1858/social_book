from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('login', views.blog_login, name='login'),
    path('register',views.blog_register, name='register'),
    path('index',views.blog_index, name='index'),
    path('sample',views.blog_sample, name='sample'),
    path('upload',views.uploadBlog, name='upload'),
    path('uploaded_blogs',views.uploaded_Blogs, name='uploaded_blogs'),
    path('likes',views.blog_likes, name='likes'),
    path('logout',views.logout_view, name='logout'),
    path('show_comments',views.show_comments, name='show_comments'),
    path('add_comments',views.add_comments, name='add_comments'),
    path('liked_users',views.liked_users, name='liked_users'),
    path('delete_comment',views.delete_comment, name='delete_comment'),
    path('update_comment',views.update_comment, name='update_comment'),
    
]

##first two lines are written for below if condition.If is used for mapping url path of file upload.
# Also, see the configurations made in settings.py for it. i.e.  MEDIA_ROOT=os.path.join(BASE_DIR,"media")
# and MEDIA_URL="/media/"
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)