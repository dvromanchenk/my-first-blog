from django import forms
from django.contrib.auth import authenticate

from .models import Post, User, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'short_text', 'text', 'category')


class PostShortForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'short_text')


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('email', 'password',)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный логин или пароль")
            if not self.user.is_active:
                raise forms.ValidationError("Ползователь не активен")
        return self.cleaned_data

    def get_user(self):
        return self.user


class CreateUserForm(forms.ModelForm):

    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'skype', 'avatar')


class PersonalUserForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'skype', 'avatar')


class UserInfoForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)
    first_name = forms.CharField(disabled=True)
    last_name = forms.CharField(disabled=True)
    phone = forms.CharField(disabled=True)
    skype = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'skype')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class SearchForm(forms.Form):
    search = forms.CharField(label='search', max_length=100)
