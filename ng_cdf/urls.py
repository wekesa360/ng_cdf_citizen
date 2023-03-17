from django.urls import path, include
from .views import (
    admin_view,
    projects_view,
    # add_project_view,
    bursaries_view,
    admin_bursary_view,
    admin_project_view,
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
    path('', home_view, name='home'),
    path('ng_cdf/admin/dashboard', admin_view, name='dashboard'),
    path('ng_cdf/admin/projects', admin_project_view, name='projects'),
    path('ng_cdf/admin/bursary', admin_bursary_view, name='bursary'),
]
