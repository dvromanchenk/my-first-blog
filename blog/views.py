from django.core.checks import messages
from django.shortcuts import render
from django.utils import timezone
from .models import Post, User
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, LoginForm, CreateUserForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def post_list(request):
    posts = Post.objects.order_by('published_date')
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
            return redirect('post_list')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    form = LoginForm()
    logout(request)
    #return render(request, 'blog/login.html')
    return render(request, 'blog/login.html', {'form': form})


def new_user_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                #form.cleaned_data['first_name'],
                form.cleaned_data['email'],
                form.cleaned_data['password'],
                # form.cleaned_data['last_name'],
                # form.cleaned_data['phone'],
                # form.cleaned_data['skype'],
                # form.cleaned_data['avatar'],
            )
            user.save()
            # Redirect to a success page.
            return redirect('post_list')
    else:
        form = CreateUserForm()
    return render(request, 'blog/login.html', {'form': form})
