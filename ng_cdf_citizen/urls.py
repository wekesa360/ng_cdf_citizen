"""ng_cdf_citizen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ng_cdf_api import urls as ng_cdf_api_urls
from ng_cdf import urls as ng_cdf_urls
from accounts import urls as accounts_urls
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include('rest_framework.urls')),
    path("ng_cdf-api/", include((ng_cdf_api_urls, 'ng_cdf_api'), namespace='ng_cdf-apis')),
    path("", include((ng_cdf_urls, 'ng_cdf'), namespace='ng_cdf')),
    path("accounts/", include((accounts_urls, 'accounts'), namespace='accounts'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
