from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from accounts.utils import get_authenticate_user, create_user_account
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, user_logged_out
