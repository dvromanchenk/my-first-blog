from django.contrib import messages
from django.utils import timezone
from .models import Post, User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, LoginForm, CreateUserForm, PersonalUserForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout


# Create your views here.


def post_list(request):
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
        form = CreateUserForm(request.POST)
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
        form = PersonalUserForm(request.POST, instance=request.user)
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

