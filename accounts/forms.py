from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import (
    Location
)

User = get_user_model()

class PrettyAuthenticationForm(AuthenticationForm):
    """_summary_

    Args:
        AuthenticationForm (_type_): _description_
    """
    def __init__(self, *args,**kwargs) -> None:
        """_summary_
        """
        super(PrettyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', })
        self.fields['password'].widget.attrs.update({'class': 'form-control',})

class ChangeImageForm(forms.Form):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    avatar_image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': False, 'class': 'form-control'}))

class PrettyUserCreationForm(UserCreationForm):
    """_summary_

    Args:
        UserCreationForm (_type_): _description_
    """

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), max_length=32, help_text='First name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), max_length=32, help_text='Last name')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), max_length=64, help_text='Enter a valid email address')
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'multiple': False, 'class': 'form-control'})) 
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    bio = forms.Textarea()
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = ('first_name', 'last_name', 'email', 'bio', 'location', 'avatar')


class ChangePasswordForm(forms.Form):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))