from django.shortcuts import render,redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import datetime
from .forms import *
from .models import *
import random



def blogs_list(request):
    """Страница со списком всех блогов"""
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 2)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'blog_page/blogs_list.html', context={'blogs': blogs, 'page': page})

def blog_detail(request, blog_id):
    """Страница блога со всеми постами"""
    blog = get_object_or_404(Blog, id = blog_id)
    all_post = blog.post_set.all()
    if request.user != blog.author.user:
        all_post = all_post.exclude(attr_to_view=False)
    paginator = Paginator(all_post, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog_page/blog_detail.html', context={'blog': blog, 'posts': posts, 'page': page})


def post_detail(request, blog_id, post_id):
    """Страница поста"""
    blog = get_object_or_404(Blog, id = blog_id)
    post = get_object_or_404(blog.post_set, id = post_id)
    if request.user.is_authenticated:
        guest = request.user.blogauthor
    else:
        guest = None
    Statistic.objects.create(ip_adres= request.META.get('REMOTE_ADDR'), guest= guest, date_visit= datetime.now(),
                             view_post= post , entry_page= request.META.get('HTTP_REFERER'))
    sum_views = post.statistic_set.count()
    comment = post.comment_set.all()
    sum_comment = comment.count()
    return render(request, 'blog_page/post_detail.html', context={'post': post, 'comment': comment, 'blog': blog,
                            'sum_comment': sum_comment, 'sum_views': sum_views})

def registration(request):
    """Регистрация пользователя и отправка ему пароля на почту"""
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save(commit=False)
            password_for_user = ''.join([random.choice(list
            ('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(12)])
            user.set_password(password_for_user)
            user.save()
            send_mail(subject= "Твой пароль.", message= password_for_user, from_email= "You'r blog",
                      recipient_list= [user.email])
            blog_author = BlogAuthor(user= user)
            blog_author.save()
            return redirect('blogs_list')
        else:
            return render(request, 'blog_page/registration.html', context={'registration_form':registration_form})
    else:
        registration_form = RegistrationForm()
        return render(request, 'blog_page/registration.html', context={'registration_form': registration_form})

def log_in(request):
    """Логирование пользователя"""
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, username= login_form.cleaned_data['username'],
                                password= login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('blogs_list')
            else:
                messages.add_message(request, messages.ERROR, "Неверный логин/пароль")
                return render(request, 'blog_page/log_in.html', context={'login_form': login_form})
        else:
            return render(request, 'blog_page/log_in.html', context={'login_form': login_form})
    else:
        login_form = LoginForm()
        return render(request, 'blog_page/log_in.html', context={'login_form': login_form})

def log_out(request):
    """Выход авторизованного пользователя из системы"""
    logout(request)
    return redirect('blogs_list')

def create_new_blog(request):
    """Создание нового блога"""
    if request.method == 'POST':
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.author = request.user.blogauthor
            blog.save()
            return redirect('blog_detail', blog_id=blog.id)
        else:
            return render(request, 'blog_page/create_new_blog.html', context={'blog_form': blog_form})
    else:
        blog_form = BlogForm()
        return render(request, 'blog_page/create_new_blog.html', context={'blog_form': blog_form})

def create_new_post(request, blog_id):
    """Создание нового поста"""
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.blog = blog
            post.author = request.user.blogauthor
            post.save()
            return redirect('post_detail',blog_id=blog.id, post_id= post.id)
        else:
          return render(request, 'blog_page/create_new_post.html', context={'post_form': post_form})
    else:
        post_form = PostForm()
        return render(request, 'blog_page/create_new_post.html', context={'post_form': post_form})

def create_new_comment(request, blog_id, post_id):
    """Создание нового комментария"""
    post = get_object_or_404(Post, id=post_id)
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            author = request.user
            commt_form = CreateNewCommentForAuthUser(request.POST)
        else:
            commt_form = CreateNewCommentForUnknownUser(request.POST)
            author = None
        if commt_form.is_valid():
            comment = commt_form.save(commit=False)
            comment.author_comment = author

            comment.blog = post
            comment.save()
        print(commt_form.errors)
    return redirect('post_detail', blog_id=blog.id, post_id=post.id)















