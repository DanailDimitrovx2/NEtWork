from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Write something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",)

    class Meta:
        model = Post
        fields = ['body']
        exclude = ("user", )


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']