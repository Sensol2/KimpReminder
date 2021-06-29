

# 스케쥴러, 웹푸시 모듈
from app.scheduler import start_schedule
from app.webpusher import episode_webpush

from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create scheduler to run in a thread inside the application process

def hello(request):
    print("Hello")
    # start_schedule()
    episode_webpush()
    return render(request, 'hello.html')

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', { 'posts': posts })

@login_required
def new(request):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            author = request.user
        )
        return redirect('detail', new_post.pk)
    return render(request, 'new.html')

def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if (request.method == 'POST'):
        Comment.objects.create(
            post = post, 
            content = request.POST['content'],
            author = request.user
        )
        return redirect('detail', post_pk)

    return render(request, 'detail.html', {'post': post})

def edit(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if request.method == 'POST':
        Post.objects.filter(pk=post_pk).update(
          title = request.POST['title'],
          content = request.POST['content']
        )
        return redirect('detail', post_pk)

    return render(request, 'edit.html', {'post': post}) 

def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.delete()
    return redirect('home')

def delete_comment(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('detail', post_pk)

def signup(request):
    if (request.method == 'POST'):
        found_user = User.objects.filter(username=request.POST['username'])
        if (len(found_user) > 0):
            error = 'username이 이미 존재합니다'
            return render(request, 'registeration/signup.html', {'error' : error})
        new_user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        auth.login(request, new_user)
        return redirect('home')
    return render(request, 'registeration/signup.html')

def login(request):
    if (request.method == 'POST'):
        found_user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if (found_user is None):
            error = '아이디 또는 비밀번호가 틀렸습니다'
            return render(request, 'registeration/login.html', {'error' : error})

        auth.login(request, found_user)
        return redirect('home')
    return render(request, 'registeration/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')