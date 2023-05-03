from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    # path('profile/', views.profile_view, name='profile'),
    path('profile/', views.admin_edit_profile_view, name='profile_edit'),
    path('profile/', views.admin_edit_profile_view, name='user_profile_edit'),
    path('profile/<str:username>/delete/', views.delete_profile_view, name='profile_delete'),
    path('profile/<str:username>/change-password/', views.change_password_view, name='change_password'),
    path('profile/<str:username>/change-image/', views.change_image_view, name='change_image'),
]

