from warnings import filters
from django.contrib import messages
from django.shortcuts import render, redirect
#from rest_framework import *
import math,random



from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect

from .serializers import CustomUserSerializer, ProfileSerializer,ProfileUpdateSerializer

from .forms import UploadFileForm
from .models import CustomUser, Profile
from django.utils import timezone
from django.shortcuts import render
from .models import UploadedFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
# from django_filters.rest_framework import SearchFilter
# from rest_framework.filters import SearchFilter
# from rest_framework import filters
from rest_framework import generics
import django_filters
from django_filters import rest_framework as filters
from django.core.mail import send_mail




@csrf_protect
def login_run(request):
    if request.method=="POST":
         uname=request.POST.get('username')
         password=request.POST.get('password')
         user = authenticate(request, username=uname, password=password)
         if user is not None:
             ## Two step authentication via sending OTP after logging in
             OTP=generateOTP()
             print(OTP)
             request.session['OTP'] = OTP
             request.session.save()
             send_mail(
                'OTP for login:',
                f'Your OTP for login is :{OTP}',
                'sstesting64@gmil.com',
                [user.email],
                fail_silently=False,
            )
             login(request,user)
             return redirect('sendOTP')
         else:
             messages.error(request,'username or password not correct or empty')
            #  return HttpResponse("username or password is incorrect")
    return render(request,'Application/login.html')

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


@csrf_protect
def register_run(request):
    if request.method=='POST':
        print("Inside register view of app")
        email=request.POST.get('email')
        username=request.POST.get('username')
        pass1=request.POST.get('password')
        pass2=request.POST.get('confirmPassword')
        publicVisibility = request.POST.get("publicVisibility")
        address = request.POST.get("address")
        birthYear = request.POST.get("birthYear")

        print(publicVisibility)

        if publicVisibility == 'on':
            publicVisibility = True
        else:
             publicVisibility = False

        today =  timezone.now()
        age = today.year - int(birthYear)


        if pass1 != pass2:
            messages.error(request,'your password and confirm password should match')
        elif email=="" or username=="" or pass1=="" or pass2=="":
             messages.error(request,'please fill mandatory fields like email, uname, password, confirm password')
        else:
            newuser = CustomUser.objects.create_user(email,pass1, username, publicVisibility, address, birthYear, age)
            newuser.save()
            send_mail(
            'Registration Confirmation',
            'Thank you for registering on social_book',
            'sstesting64@gmail.com',
            [email],
            fail_silently=False,
        )
          
            #messages.success(request, 'Form submission successful')
            return redirect('login')
            
    return render(request,'Application/register.html')

def otpVerification_run(request):
    if request.method=="POST":
        otp = request.POST.get('OTP')
        print("otp:",otp)
        sessionOTP = request.session.get('OTP')
        print("session otp:",sessionOTP)
        if otp == sessionOTP:
            return redirect('index')
        else:
            messages.error(request,'entered otp is invalid !!!!')
    return render(request,'Application/otpVerification.html')

def index_run(request):
        return render(request,'Application/index.html')

def authorsAndSellers_run(request):
    filteredCustomers=None
    if request.method == 'POST':
        publicVisibility = request.POST.get('publicVisibility')
        print("publicVisibility",publicVisibility)
        userStatus = request.POST.get('user_status')
        if publicVisibility == 'on':
            # filteredCustomers = CustomUser.objects.filter(publicVisibility=1)
            if userStatus == '1' :
                filteredCustomers = CustomUser.objects.filter(is_active=1,publicVisibility=1)

            elif userStatus == '0':
                filteredCustomers = CustomUser.objects.filter(is_active=0,publicVisibility=1)

            elif userStatus == '2':
                filteredCustomers = CustomUser.objects.filter(publicVisibility=1)

        elif publicVisibility is None:
             if userStatus == '1' :
                filteredCustomers = CustomUser.objects.filter(is_active=1,publicVisibility=0)

             elif userStatus == '0':
                filteredCustomers = CustomUser.objects.filter(is_active=0,publicVisibility=0)

             elif userStatus == '2':
                filteredCustomers = CustomUser.objects.filter(publicVisibility=0)
    else:
        filteredCustomers = None
        return render(request,'Application/authorsAndSellers.html', {'CustomUsers': filteredCustomers})
    # print("filteredCustomers",filteredCustomers)
    return render(request,'Application/authorsAndSellers.html', {'CustomUsers': filteredCustomers})

def forgot_password_run(request):
    return render(request,'Application/forgot-password.html')

def uploadFile_run(request):
    # submitted=False
    # user=CustomUser.objects.get(id=request.user.id)
    current_user=request.user ##instance of current logged in user is taken
    id=current_user.id
    print(type(id))
    print("id",id)
    initial_data={
        'user':id,
        'cost':'0.0',
    }
    if request.method=='POST':
        fm=UploadFileForm(request.POST,request.FILES ) #resuest.FILES is very imp as it will take care of
        #storing the files at defined location
        
        if fm.is_valid():
            fm.save()
            # return HttpResponseRedirect('uploadFile?submitted=True')
            return redirect('uploadFile')
    
    else:
        fm=UploadFileForm(initial=initial_data)   
        return render(request,'Application/uploadFile.html', {'form':fm})
    # return render(request,'Application/uploadFile.html', context=mydict)

def uploaded_Files_run(request):
    # files = UploadedFile.objects.all()
    # id=request.user.id
    
    ###fro reference:- solution to solve the error:-
    ###DoesNotExist at /uploaded_Files
    ###UploadedFile matching query does not exist
        ###solution:-
        ###if UserPreference.objects.filter(user = request.user).exists():
        ###currency = UserPreference.objects.get(user = request.user).currency
    ###else:
        ###currency = 'INR - Indian Rupee'



    
    # print("files object",files)
    try:
        if UploadedFile.objects.get(user=request.user):
            files = UploadedFile.objects.get(user = request.user)
            return render(request, 'Application/uploaded_Files.html', {'files': files})
    except Exception as e:
            return redirect('uploadFile')
        # return render(request,'Application/uploadFile.html', {'form':files})
    
    
        # print("Exception ",e)



def logout_run(request):
    return render(request, 'Application/login.html')


##REST frMEWORK api -REFERENCE(https://www.django-rest-framework.org/api-guide/views/)
class ListUsers(viewsets.ModelViewSet):
    # """
    # View to list all users in the system.

    # * Requires token authentication.
    # * Only admin users are able to access this view.
    # """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    ## below two lines are helpful for serializing entire list of all CustomUser objects and sending it as response
    serializer_class=CustomUserSerializer
    def get_queryset(self):
        return CustomUser.objects.all()
  

'''  Note that the default obtain_auth_token view explicitly uses JSON requests and responses, rather than using default renderer and parser classes in your settings.

By default, there are no permissions or throttling applied to the obtain_auth_token view. If you do wish to apply to throttle you'll need to override the view class, and include them using the throttle_classes attribute.

If you need a customized version of the obtain_auth_token view, you can do so by subclassing the ObtainAuthToken view class, and using that in your url conf instead.

For example, you may return additional user information beyond the token value:'''
# command for genrating tokens after version 3.6.4- ./manage.py drf_create_token <username>

# In case you want to regenerate the token (for example if it has been compromised or leaked) 
# you can pass an additional parameter:./manage.py drf_create_token -r <username>


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email
        })
    
# class CustomUserFilter(django_filters.FilterSet):
#     is_active=filters.CharFilter('is_active')
#     designation=filters.CharFilter('profile_designation')
#     min_salary=filters.CharFilter(method="filter_by_min_salary")
#     max_salary=filters.CharFilter(method="filter_by_max_salary")

#     class Meta:
#         fields=CustomUserfields=('is_active','designation','username')

#     def filter_by_min_salary(self,queryset,name,value):
#         queryset=queryset.filter(profile__salary__gt=value)
#         return queryset
    
#     def filter_by_max_salary(self,queryset,name,value):
#         queryset=queryset.filter(profile__salary__lt=value)
#         return queryset



class CustomerUserViewSet(viewsets.ModelViewSet):
    serializer_class=CustomUserSerializer
    queryset=CustomUser.objects.all()
    #filter_backends=(DjangoFilterBackend, OrderingFilter,filters.SearchFilter)
    # filter_backends=(DjangoFilterBackend, OrderingFilter)
    # filter_class=CustomUserFilter
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes=[JSONParser,FormParser,MultiPartParser]

    # ordering_fields=('is_active','username')
    # ordering=('username')
    # search_fields=('username','first_name')

    @action(detail=True,methods=['put'])
    def profile(self,request,  pk=None):
            print("try")
            user=self.get_object()
            # user=CustomUser.objects.get(User=request.user)
            profile=user.profile
            
            serializer=ProfileSerializer(profile,data=request.data)
        
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                return Response(serializer.errors,status=400)
        


##comment:- the problem with this method is that it can't be used to send file type of data. If field is 
## not of file type then same view can be used to read,update and delete 
# #-refernce(youtube video:-Django Rest Framework for Beginners - Simple CRUD API, channel-John Watson Rooney)

# class CustomerUserViewSet(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class=CustomUserSerializer
#     queryset=CustomUser.objects.all()
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)
#     parser_classes=[JSONParser,FormParser,MultiPartParser]

class ProfileUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes=[JSONParser,FormParser,MultiPartParser]

    def post(self,request,format='None'):
        user=request.user
        serializer=ProfileUpdateSerializer(instance=user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=200)
        else:
            return Response(data=serializer.errors,status=500)