from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager


class Post(models.Model):

    MODERATION = 'M'
    CHECKED = 'C'
    REJECTED = 'R'
    STATUSES = (
        (MODERATION, 'On moderation'),
        (CHECKED, 'Checked'),
        (REJECTED, 'Rejected')
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    short_text = models.CharField(max_length=400)
    mark = models.IntegerField(default=0)
    category = models.ForeignKey('blog.Category', null=True, blank=True, on_delete=models.PROTECT)
    status = models.CharField(choices=STATUSES, max_length=1, default=MODERATION)
    reason = models.TextField(default="", blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def change_mark(self, mark):
        self.mark += mark
        self.save()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prev_status = self.status

    def save(self, *args, **kwargs):

        if self.status != self.prev_status:
            email = self.author.email
            name = self.author.first_name

            if self.status == self.MODERATION:
                self.published_date = timezone.now()
                email_subject = 'Публикация поста'
                email_body = "Здравствуйте, %s! Ваш пост \"%s\" опубликован." % (name, self.title)
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            elif self.status == self.REJECTED:
                email_subject = 'Пост не опубликован'
                email_body = "Здравствуйте, %s! Публикация Вашего поста \"%s\" отклонена модератором." \
                             "\nПричина: %s." % (name, self.title, self.reason)
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone = models.CharField(_('phone'), max_length=12, blank=True)
    skype = models.CharField(_('skype'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True)
    confirm = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def count_rate(self):
        marks = Rating.objects.filter(post=self)
        value = 0
        for mark in marks:
            value += mark.value
        self.rate = value


class RatingManager(models.Manager):
    def create_rating(self, author, post):
        mark = self.create(author=author, post=post)
        return mark


class Rating(models.Model):
    value = models.IntegerField(default=0)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    author = models.ForeignKey('blog.User', on_delete=models.CASCADE)

    objects = RatingManager()

    def change_marks(self, mark):
        self.value = mark

    def __str__(self):
        return str(self.value)


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title