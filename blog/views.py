import hashlib

from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from mysite import settings
from .models import Post, User, Rating, Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, LoginForm, CreateUserForm, PersonalUserForm, \
    CommentForm, SearchForm, UserInfoForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout


# Create your views here.


def post_list(request):
    sort = request.GET.get('sort')
    search = request.POST.get('search')
    category = request.GET.get('category')
    category_list = Category.objects.order_by('title')
    posts = Post.objects.all()
    if search is not None and request.method == "POST":
        posts = posts.filter(Q(title__icontains=search) |
                             Q(short_text__icontains=search) |
                             Q(text__icontains=search))
    else:
        posts = posts.order_by('published_date')

    if sort == 'author':
        posts = posts.order_by('author')
    elif sort == 'date':
        posts = posts.order_by('published_date')

    if category:
        posts = posts.filter(category=category)

    if posts:
        posts = posts.filter(status=Post.CHECKED)

    return render(
        request,
        'blog/post_list.html',
        {
            'posts': posts,
            'search': search,
            'category_list': category_list,
            'category': int(category) if category else None
        }
    )


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
            post = form.save()
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
            email = form.cleaned_data['email'].lower()
            user.activation_key = hashlib.sha1(email.encode('utf-8')).hexdigest()
            user.save()

            # Send email
            host = request.get_host()
            email_subject = 'Подтверждение регистрации'
            email_body = "Здравствуйте %s, Для подтверждения регистрации перейдите по ссылке  " \
                         "http://%s/register/confirm/%s" % (user.email, host, user.activation_key)
            user.email_user(email_subject, email_body, from_email=settings.EMAIL_HOST_USER, fail_silently=False)

            # login user
            login_view(request)

            messages.add_message(request, messages.INFO, 'Сonfirm your email to activate account')

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

    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/personal_cabinet.html', {'form': form,
                                                          'posts': posts,
                                                          'author_flag': True
                                                          })


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.author = request.user.first_name+' '+request.user.last_name
            else:
                comment.author = 'Anonymus'
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
    else:
        messages.add_message(request, messages.INFO, 'You already rate this post')
    return redirect('post_detail', pk=pk)


def confirm_account(request, key):

    user = get_object_or_404(User, activation_key=key)
    user.confirm = True
    user.save()

    messages.add_message(request, messages.INFO, 'Email confirmed, account activated')

    if request.user.is_authenticated:
        return redirect('personal_cabinet')
    else:
        return redirect('login')


def post_delete(request, pk):
    Post.objects.get_or_404(pk=pk).delete()
    return redirect('post_list')


def user_list(request):
    users = User.objects.all()
    return render(request, 'blog/user_list.html', {'users': users})


def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    form = UserInfoForm(instance=user)
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/personal_cabinet.html', {'form': form,
                                                          'posts': posts,
                                                          'user': user,
                                                          'author_flag': True,
                                                          'info_flag': True
                                                          })