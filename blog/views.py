from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView

from .models import Post, User, Rating
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, LoginForm, CreateUserForm, PersonalUserForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout


# Create your views here.


def post_list(request):
    sort = request.GET.get('sort')
    if sort == 'author':
        posts = Post.objects.order_by('author')
    else:
        posts = Post.objects.order_by('published_date')

    if posts is None:
        messages.add_message(request, messages.INFO, 'No posts')

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Redirect to a success page.
            return redirect('personal_cabinet')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def new_user_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            # Redirect to a success page.
            return redirect('post_list')
    else:
        form = CreateUserForm()
    return render(request, 'blog/login.html', {'form': form})


def personal_cabinet(request):
    if request.method == "POST":
        form = PersonalUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Data saved')
    else:
        form = PersonalUserForm(instance=request.user)
    return render(request, 'blog/personal_cabinet.html', {'form': form})


def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    if posts is None:
        messages.add_message(request, messages.INFO, 'No posts')

    return render(request, 'blog/post_list.html', {'posts': posts})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def mark_to_post(request, pk):
    post = Post.objects.get(pk=pk)
    rating, created = Rating.objects.get_or_create(post=post, author=request.user)

    if created:
        mark = int(request.GET.get('mark'))
        rating.change_marks(mark=mark)
        post.change_mark(mark=mark)

        rating.save()
        post.save()
    else:
        messages.add_message(request, messages.INFO, 'You already rate this post')
    return redirect('post_detail', pk=pk)

