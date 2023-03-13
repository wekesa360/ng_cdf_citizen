from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import PrettyAuthenticationForm, PrettyUserCreationForm, ChangeImageForm, ChangePasswordForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from ng_cdf.views import check_if_admin


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
                user = get_user_model().objects.get(email=email)
                ng_cdf = check_if_admin(user)
                if ng_cdf is None:
                    messages.info(request, f'You are logged in!')
                    return redirect('ng_cdf:home')
                else:
                    messages.info(request, f'You are logged in!')
                    return redirect('admin:dashboard')
            else:
                messages.error(request, 'invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    form = PrettyAuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})

def signup_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    if request.method == 'POST':
        form = PrettyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('nd_cdf:home')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = PrettyUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signout_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('nd_cdf:home')

@login_required
def profile_view(request, username):
    """_summary_

    Args:
        request (_type_): _description_
        username (_type_): _description_
    """
    try:
        user = get_user_model().objects.get(username=username)
    except ObjectDoesNotExist:
        messages.error(request, 'User not found')
        return redirect('nd_cdf:home')
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def edit_profile_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    if request.method == 'POST':
        form = PrettyUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:profile', request.user.username)
        else:
            messages.error(request, 'Unsuccessful. Invalid information.')
    form = PrettyUserCreationForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def delete_profile_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Profile deleted successfully')
        return redirect('nd_cdf:home')
    return render(request, 'accounts/delete_profile.html')

@login_required
def change_image_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    if request.method == 'POST':
        form = ChangeImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.avatar = form.cleaned_data.get('avatar_image')
            user.save()
            messages.success(request, 'Image changed successfully')
            return redirect('accounts:profile', user.username)
        else:
            messages.error(request, 'Unsuccessful. Invalid information.')
    form = ChangeImageForm()
    return render(request, 'accounts/change_image.html', {'form': form})

@login_required
def change_password_view(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    form = ChangePasswordForm()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data.get('old_password')
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            if user.check_password(old_password) == user.check_password(new_password):
                messages.error(request, 'New password must be different from old password')
                redirect('accounts:change_password')
            if user.check_password(current_password) and user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully')
                return redirect('accounts:profile', user.username)
            else:
                messages.error(request, 'Old password is incorrect')
    return render(request, 'accounts/change_password.html')