from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils import timezone

# Create your views here.
@csrf_protect
def login_run(request):
    if request.method=="POST":
         uname=request.POST.get('username')
         password=request.POST.get('password')
         user = authenticate(request, username=uname, password=password)
         if user is not None:
             login(request,user)
             return redirect('index')
         else:
             messages.error(request,'username or password not correct or empty')
            #  return HttpResponse("username or password is incorrect")
    return render(request,'Application/login.html')

@csrf_protect
def register_run(request):
    if request.method=='POST':
        email=request.POST.get('email')
        uname=request.POST.get('username')
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
        elif email=="" or uname=="" or pass1=="" or pass2=="":
             messages.error(request,'please fill mandatory fields like email, uname, password, confirm password')
        else:
            newuser = CustomUser.objects.create_user(email,pass1, uname, publicVisibility, address, birthYear, age)
            newuser.save()
            #messages.success(request, 'Form submission successful')
            return redirect('login')
            
    return render(request,'Application/register.html')

def index_run(request):
    return render(request,'Application/index.html')


        

        # uname=request.POST.get('username')
        # pass1=request.POST.get('password')
        # pass2=request.POST.get('confirmPassword')
        # fullName=request.POST.get('fullName')
        # gender=request.POST.get('gender')
        # city=request.POST.get('city')
        # state=request.POST.get('state')
        # cardType=request.POST.get('cardType')
        # cardNumber=request.POST.get('cardNumber')
        # cvc=request.POST.get('cvc')
        # month=request.POST.get('month')
        # year=request.POST.get('year')
        # print(uname)