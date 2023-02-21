from django.shortcuts import render, get_list_or_404, redirect
from django.contrib import messages
import uuid as  unique_gen
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def user_view(request):
    user = User.objects.get(email=request.user.email)
