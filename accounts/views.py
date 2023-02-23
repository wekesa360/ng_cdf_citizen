from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import PrettyAuthenticationForm, PrettyUserCreationForm, ChangeImageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def signin_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    if request.method == 'POST':
        form = PrettyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                #send email
                messages.info(request, f'You are logged in!')
                return redirect('nd_cdf:home')
            else:
                messages.error(request, 'invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    form = n