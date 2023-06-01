from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Blogger,UploadedBlogs,Comments
from .forms import UploadBlogForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core import serializers
from datetime import datetime
from django.core.serializers import serialize
from django.core.paginator import Paginator



from django.contrib.auth import logout
# from .models import Likes,Comments
# Create your views here.

@csrf_protect
def blog_register(request):
    print("Inside register of blog")
    if request.method=='POST':
        email=request.POST.get('email')
        print("email:",email)
        username=request.POST.get('username')
        print("username:",username)
        password=request.POST.get('pass')
        print("password:",password)
        newuser =Blogger.objects.create_blogger(email,password, username)
        newuser.save()
        
        return redirect('login')
    else:

         return render(request,'Blog/register.html')

@csrf_protect
def blog_login(request):

    if request.method=="POST":
         print("inside login view")
         uname=request.POST.get('username')
         print("uname",uname)
         password=request.POST.get('pass')   
         print("password",password)         
        #  user = authenticate(request, username=uname, password=password)
         
         try:
            user=Blogger.objects.get(username=uname,password=password)
            if Blogger.objects.filter(username=uname,password=password).exists():
                #  login(request,user)
                print("logged user id:",user.id)
                request.session['id']=user.id
                request.session['username']=user.username
                print("username",user.username)
                return JsonResponse({'status':'success','url':'index'})
            if Blogger.DoesNotExist:
                return JsonResponse({'status':'error','url':'login'})
         except Blogger.DoesNotExist : 
             return JsonResponse({'status':'error','url':'login'})
    if request.method=="GET":
        return render(request,'Blog/login.html')

@csrf_protect
def blog_sample(request):
    return render(request,'Blog/sample.html')

def logout_view(request):
    print("Session deleted",request.session['id'])
    del request.session['id']
    return redirect('login')


# @login_required(login_url='login')
@csrf_protect
def blog_index(request):
    print("Inside get method of index view")

    try:
        # all the UploadedBlogs objects will be arranged in descending order of their primary key due to order_by('-id')
        blogs=UploadedBlogs.objects.all().order_by('-id')

        # Create a Paginator object with the objects and the desired number of items per page
        paginator = Paginator(blogs, 10)  # 10 objects per page

        print("paginator",paginator)

        # Get the current page number from the request parameters
        page_number = request.GET.get('page')

        # Get the objects for the current page
        page_objects = paginator.get_page(page_number)

        print(type(blogs))
        print("allblogs",blogs)
        userid=request.session['id']
        print("id",userid)
        user=Blogger.objects.filter(id=userid)
        print("user",user)
        
        # print(type(user))
        # print("Username",user.username)
        # print("Username:",username)
        print(userid,type(userid),blogs[0].user_id,type(blogs[0].user_id))
        # return render(request,'Blog/index.html',{'blogs':blogs,'user':user,'userid':userid})

        return render(request,'Blog/index.html',{'page': page_objects,'user':user,'userid':userid})



    except Exception as e:
        print("Exception is:",e)
        return render(request,'Blog/login.html')

@csrf_protect
def uploadBlog(request):
    fm=None
    print("request",request)
    
    try:
        logged_user=request.session['id']
        print("logged user",logged_user)
        user=Blogger.objects.filter(id=logged_user)
        print(user)
        if request.method=='POST':
            initial_data=None
            
            fm=UploadBlogForm(request.POST,request.FILES ) #resuest.FILES is very imp as it will take care of
            
            if fm.is_valid():
                

                fm.save()
                # obj.user = request.user
                # obj.save()
                print("request",request)
                print("request user",request.user)
                print("Inside form validation")
                # blogs=UploadedBlogs.objects.all().values()
                # print("blogs",blogs)
                messages.success(request,"Your Blog is uploaded successfully.Go on home page to view it.")
                # return render(request,'Blog/upload.html',{'blogs':blogs,'form':fm})
                return render(request,'Blog/upload.html',{'form':fm})
        
            else:
                print("fm.errors",fm.errors)
                print("Inside else condition for invalid form")
                fm=UploadBlogForm(initial=initial_data)   
                return render(request,'Blog/upload.html', {'form':fm,'user':user})
            
        elif request.method=='GET' :
            print("Inside get method of upload view")
            current_datetime=datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
            # current_user=request.user
            # id=current_user.id
            # print("id",id)
            # logged_user is obtained through session variable which is storing the currently logged in user
            initial_data={
                'user':logged_user,
                'title':'name',
                'description':'desc',
                'time':formatted_datetime,
            }
        
            fm=UploadBlogForm(initial=initial_data)  
            # print("user",user.id)
            return render(request,'Blog/upload.html', {'form':fm,'user':user})
    except Exception as e:
        print("Exception is:",e)
        return redirect('login')
    
@csrf_protect
def uploaded_Blogs(request):
    pass

@csrf_protect
def blog_likes(request):
    # blogs=get_object_or_404(UploadedBlogs,id=request.POST.get('blog_id'))
    # logged_user=request.session['id']
    # is_liked=False

    # if blogs.likes.filter(id=logged_user).exists():
    #     blogs.likes.remove(logged_user)
    #     is_liked=False
    
    # else:
    #     blogs.likes.add(logged_user)
    #     is_liked=True
    
    # # blogs.likes.add(logged_user)
    # return redirect('index')
    if request.method=='POST':
        Like=False
        id=request.POST.get('blog_id')
        logged_user=request.session['id']
        # bcount=request.POST.get('bcount')
        print("id",id)
        get_blog=get_object_or_404(UploadedBlogs,id=id)
        print("Get Blog",get_blog)
        print("logged user",logged_user)
        if  get_blog.likes.filter(id=logged_user).exists():
            print("in logged in user exists in likes ")
            get_blog.likes.remove(logged_user)
            Like=False
        else:
            print("in logged in user  doesn't exists in likes ")
            get_blog.likes.add(logged_user)
            Like=True

        data={
            "liked":Like,
             "likes_count":get_blog.likes.all().count()
         }

        return JsonResponse(data,safe=False)
    return redirect('index')


        # print("bcount",bcount)
    #     try:
    #         # if Likes.objects.filter(blog_id=id).exists():
    #         print("Inside likes exist")
    #         likes=Likes.objects.get(blog_id=id)
    #         likes.count=likes.count-1
    #         likes.save()
    #         print("likes count:",likes.count)
    #         return JsonResponse({'status':'added','count':likes.count})
    #     except Likes.DoesNotExist:
    #             print("Inside likes does not exist")
    #             count=1
    #             # newlikes =Likes.objects.create(blog_id=id,count=count)
    #             newlikes =Likes.objects.create_Likes(blog_id=id,count=count)
    #             newlikes.save()
    #             print("likes count:",newlikes.count)
    #             return JsonResponse({'status':'created','count':newlikes.count})
    # # elif request.method=='GET':
    # print("outside except")
    # return JsonResponse({'status':'get'})

def show_comments(request):
    if request.method=='POST':
        print("Inside psot of show comments")
        id=request.POST.get('blog_id')
        logged_id=request.session['id']
        user=Blogger.objects.get(id=logged_id)
        print("user",user)
        username=user.username
        print("username",username)
        print("blog id",id)
        if Comments.objects.filter(blog_id=id).exists():
            queryset=Comments.objects.filter(blog_id=id)
            status=True
            # print("Comments in queryset",queryset.comments)
            # queryset=Comments.objects.filter(blog_id=id).values_list('comments', flat=True)
            data=serializers.serialize('json',queryset)
            # user=serialize('json',user)
            # comments=list(comments)
        
        elif Comments.DoesNotExist:
            data="No Comments to show"
            status=False

        data={
             "comments":data,
             "status":status,
             "username":username,
         }

        return JsonResponse(data,safe=False)

def add_comments(request):
    if request.method=='POST':
        print("Inside post of add comments")
        id=request.POST.get('blog_id')
        blog=UploadedBlogs.objects.get(id=id)
        print("blog id",id)
        comments=request.POST.get('text')
        print("text:",comments)
        logged_user=request.session['id']
        print("logged_user",logged_user)
        blogger=Blogger.objects.get(id=logged_user)
        username=blogger.username
        newcomment =Comments.objects.create_comments(blog,comments,username)
        newcomment.save()


        logged_id=request.session['id']
        user=Blogger.objects.get(id=logged_id)
        print("user",user)
        username=user.username
        print("username",username)

        # adding show comment functionality also so that all comments will be shown automatically after adding
        if Comments.objects.filter(blog_id=id).exists():
            queryset=Comments.objects.filter(blog_id=id)
            status=True
            # print("Comments in queryset",queryset.comments)
            # queryset=Comments.objects.filter(blog_id=id).values_list('comments', flat=True)
            data=serializers.serialize('json',queryset)
            # comments=list(comments)
        
        elif Comments.DoesNotExist:
            data="No Comments to show"
            status=False

        data={
             "comments":data,
             "status":status,
             "username":username
         }

        return JsonResponse(data,safe=False)
    else:
        return JsonResponse({'status':'failed'},safe=False)

def liked_users(request):
    if request.method=='POST':
        print("Inside post of liked users")
        blog_id=request.POST.get('blog_id')
        print("Blog id",blog_id)

        names=[]

        # rerurning multiple objects-i.e. queryset
        blogs=UploadedBlogs.objects.filter(id=blog_id)
        # accessing likes fields(which is manytomany mapped) for each blog object
        for item in blogs:
            # below query gives names with their values of all the fields of items field which is many to many mapped
            likes=item.likes.values()
            for like in likes:
                names.append(list(like.values())[1])
            
            print("likes",likes,type(likes),len(likes))

        # for items in names:
        print("names items",names)

        # serializing likes queryset which is showing names of all users who liked the blog
        # data=serializers.serialize('json',names)
        # data={
        #      "names":data
        #  }
        # # print("data",data.names)
    return JsonResponse({'names':names})

def delete_comment(request):
    if request.method=='POST':
        comments=None
        print("Inside post method of delete comments")
        comment=request.POST.get('comment')
        
        print("comment obtained is:",comment)

        logged_user=request.session['id']
        user=Blogger.objects.get(id=logged_user)
        name=user.username
        print("commented user:",name)

        comment_obj=Comments.objects.get(comments=comment,username=name)
        print("comment_obj:",comment_obj)
        # deleting comment object
        comment_obj.delete()

        logged_id=request.session['id']
        user=Blogger.objects.get(id=logged_id)
        print("user",user)
        username=user.username
        print("username",username)

        blog_id=request.POST.get('blog_id')
        if Comments.objects.filter(blog_id=blog_id).exists():
            queryset=Comments.objects.filter(blog_id=blog_id)
            comments=serialize('json',queryset)
            status=True

        elif Comments.DoesNotExist:
            data="No Comments to show"
            status=False

        data={
            "comments":comments,
            "status":status,
            "username":username
        }
        return JsonResponse(data,safe=False)
    
def update_comment(request):
    if request.method=='POST':
        print("Inside post method of update comments")
        comment=request.POST.get('comment')
        id=request.POST.get('blog_id')
        print("blog id:",id)
        old_comment=request.POST.get('old_comment')
        print("old comment:",old_comment)
        new_comment=request.POST.get('new_comment')
        print("new comment:",new_comment)
        username=request.POST.get('username')
        print("username is:",username)

        current_obj = Comments.objects.get(username=username,comments=old_comment)
        print("present object is:",current_obj)
        current_obj.comments = new_comment
        current_obj.save()

        if Comments.objects.filter(blog_id=id).exists():
            queryset=Comments.objects.filter(blog_id=id)
            status=True
            # print("Comments in queryset",queryset.comments)
            # queryset=Comments.objects.filter(blog_id=id).values_list('comments', flat=True)
            data=serializers.serialize('json',queryset)
            # user=serialize('json',user)
            # comments=list(comments)
        
        elif Comments.DoesNotExist:
            data="No Comments to show"
            status=False

        data={
             "comments":data,
             "status":status,
             "username":username,
         }

        return JsonResponse(data,safe=False)
    
    