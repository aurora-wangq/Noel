from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.template import loader
# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile, Post, Comment
from django.contrib.auth.decorators import login_required
from .forms import Userfile
from datetime import datetime

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
        if show_view == 'true':
            show_view = True
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

# @login_required(login_url='fan:login')
# def editavatar_view(request):
#     user_object = User.objects.get(username=request.user.username)
#     user_profile = UserProfile.objects.get(owner=user_object)
#     if request.method == 'POST':
#         user_profile.img = request.FILES.get('avatar')
#         user_profile.save()
#         return redirect('fan:home')
#     else:
#         return render(request, 'fan/editavatar.html')

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
        "nike_name": post.owner_profile.nike_name,
        "username": post.post_owner.username,
        "title": post.owner_profile.title,
        "user_profile": post.owner_profile,
    }
    if request.method == 'POST':
        text = request.POST['comment_text']
        new_comment = Comment.objects.create(user=user_profile, post=post, text=text)
        new_comment.save()
        return redirect('fan:post_detail', post_id=post_id)
    else:
        return render(request, 'fan/article_detail.html', context)


@login_required(login_url='fan:login')
def user_page_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(owner=user_object)
    context = {
        "backimg": user_profile.back_img,
        "nike_name": user_profile.nike_name,
        "title": user_profile.title,
        "username": user_object.username,
        "sign": user_profile.sign,
        "birthday": user_profile.birthday,
        "address": user_profile.address,
        "desc": user_profile.desc,
        "uid": user_object.id,
        "avatar": user_profile.img,
    }
    return render(request, 'fan/user_page.html', context)

@login_required(login_url='fan:login')
def logout_view(request):
    logout(request)
    return redirect('fan:login')

@login_required(login_url='users:login')
def edit_profile_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(owner=user_object)
    user_profile1 = UserProfile.objects.get(owner=user_object)
    context = {
        "nike_name": user_profile.nike_name,
        "sign": user_profile.sign,
        "address": user_profile.address,
        "desc": user_profile.desc,
        "birthday": user_profile.birthday
    }
    if request.method == 'POST':
        if request.POST['nike_name']:
            user_profile.nike_name = request.POST['nike_name']
        else:
            user_profile.nike_name = user_profile1.nike_name
        if request.POST['desc']:
            user_profile.desc = request.POST['desc']
        else:
            user_profile.desc = user_profile1.desc
        if request.POST['sign']:
            user_profile.sign = request.POST['sign']
        else:
            user_profile.sign = user_profile1.sign
        if request.POST['address']:
            user_profile.address = request.POST['address']
        else:
            user_profile.address = user_profile1.address
        if request.FILES.get('img'):
            user_profile.img = request.FILES.get('img')
        else:
            user_profile.img = user_profile1.img
        if request.FILES.get('backimg'):
            user_profile.back_img = request.FILES.get('backimg')
        else:
            user_profile.back_img = user_profile1.back_img
        user_profile.save()
        if request.POST['birthday']:
            user_profile.birthday = datetime.datetime.strptime(request.POST['birthday'], "%")
            print(request.POST['birthday'])
        else:
            user_profile.birthday = user_profile1.birthday
        return redirect('fan:user_page')
    else:
        return render(request, 'fan/edit_user.html', context)