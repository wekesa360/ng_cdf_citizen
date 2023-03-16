from django.urls import path, include
from .views import (
    admin_view,
    projects_view,
    # add_project_view,
    bursaries_view,
    admin_bursary_view,
    # add_citizen_report_view,
    apply_bursary_view,
    citizen_report_view,
    home_view,
    # add_citizen_report_view,
    delete_report_view,
    delete_bursary_view,
    delete_project_view,
    edit_bursary_view,
    edit_project_view,
    edit_report_view
)


urlpatterns = [
    path('admin/dashboard', admin_view, name='dashboard'),
    path('', home_view, name='home'),
    path('admin/bursary', admin_bursary_view, name='bursary'),
]
