from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('login', views.login_run, name='login'),
    path('register',views.register_run, name='register'),
    path('index',views.index_run, name='index'),
    path('authorsAndSellers',views.authorsAndSellers_run, name='authorsAndSellers'),
    path('uploadFile',views.uploadFile_run, name='uploadFile'),
    path('uploaded_Files',views.uploaded_Files_run, name='uploaded_Files'),
    path('api/users',views.ListUsers.as_view({'get': 'list'})),
    path('sendOTP', views.otpVerification_run, name='sendOTP'),
    path('forgot_password', views.forgot_password_run, name='forgot_password'),

    # path for generating api token
    path('api/token/auth', views.CustomAuthToken.as_view()),
    
    path('logout', views.logout_run,name='logout'),
    path('profileupdate', views.ProfileUpdateView.as_view()),
    
]

##first two lines are written for below if condition.If is used for mapping url path of file upload.
# Also, see the configurations made in settings.py for it. i.e.  MEDIA_ROOT=os.path.join(BASE_DIR,"media")
# and MEDIA_URL="/media/"
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)