from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class LoginForm(forms.Form):
    username = forms.CharField( widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name_blog', 'description')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'preview', 'text_post', 'attr_to_view')

class CreateNewCommentForUnknownUser(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text_comment', 'email')

class CreateNewCommentForAuthUser(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text_comment',)



