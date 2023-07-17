from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.template import loader
# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile, Post, Comment
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
        user = authenticate(request, username=username, password=password)
        # Newuser = User.objects.create_user(username='John', password='123456')
        # user.save()
        # 验证如果用户不为空
        if user is not None:
            # login方法登录
            login(request, user)
            # 返回登录成功信息
            return redirect('fan:home')
        else:
            # 返回登录失败信息
            return redirect('fan:login')

    return render(request, 'fan/login.html')


@login_required(login_url='fan:login')
def home_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(owner=user_object)
    user_list = Post.objects.order_by("-id")
    user_name = user_profile.nike_name
    uid = user_object.id
    context = {
        "user_list1": user_list,
        "user_name1": user_name,
        "uid1": uid,
    }
    return render(request, 'fan/home.html', context)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        nike_name = request.POST['nike_name']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        user_model = User.objects.get(username=username)
        new_userprofile = UserProfile.objects.create(owner=user_model, nike_name=nike_name)
        new_userprofile.save()
        return redirect('fan:login')
    else:
        return render(request, 'fan/register.html')


@login_required(login_url='fan:login')
def editarticle_view(request):
    if request.method == 'POST':
        content = request.POST['content']
        show_view = request.POST.get('show_view', False)
        
        user_object = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(owner=user_object)
        new_post = Post.objects.create(post_owner=user_object, post_content=content, owner_profile=user_profile, show_view=show_view)
        new_post.post_img1 = request.FILES.get('post_img1')
        # new_post.post_img2 = request.FILES.get('post_img2')
        # new_post.post_img3 = request.FILES.get('post_img3')
        # new_post.post_img4 = request.FILES.get('post_img4')
        new_post.save()
        return redirect('fan:home')
    else:
        return render(request, 'fan/editarticle.html')

@login_required(login_url='fan:login')
def editavatar_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(owner=user_object)
    if request.method == 'POST':
        user_profile.img = request.FILES.get('avatar')
        user_profile.save()
        return redirect('fan:home')
    else:
        return render(request, 'fan/editavatar.html')

@login_required(login_url='fan:login')
def post_detail_view(request, post_id):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(owner=user_object)
    post = Post.objects.get(id=post_id)
    comment_list = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comment_list1": comment_list,
        "post_content": post.post_content,
        "nike_name": user_profile.nike_name,
        "username": user_object.username,
        "title": user_profile.title,
    }
    if request.method == 'POST':
        text = request.POST['comment_text']
        new_comment = Comment.objects.create(user=user_profile, post=post, text=text)
        new_comment.save()
        return redirect('fan:post_detial', post_id=post_id)
    else:
        return render(request, 'fan/article_detail.html', context)