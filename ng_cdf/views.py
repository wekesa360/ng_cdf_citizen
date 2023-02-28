from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import (
    NGCDFAdmin,
    Bursary,
    ApplicationDocument,
    NGCDFProjects,
    CitizenReport,
    ReportImage,
    ProjectImage
)
from .forms import (
    ReportImageForm,
    ProjectImageForm,
    CitizenReportForm,
    BursaryApplicationForm,
    ApplicationDocumentForm,
    BursaryForm,
    NGCDFProjectsForm,
    CreateNGCDFForm,
) 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def admin_view(request):
    user = request.user.username
    try:
        admin = User.objects.get(email=user)
        check_admin = NGCDFAdmin.objects.get(administrator=admin)
        ng_cdf = check_admin.ng_cdf
        bursaries = Bursary.objects.all(ng_cdf=ng_cdf)
        application_documents = ApplicationDocument.objects.all()
        ng_cdf_projects = NGCDFProjects.objects.all(ng_cdf=ng_cdf)
        citizen_report = CitizenReport.objects.all(ng_cdf=ng_cdf)
        report_images = ReportImage.objects.all()
        project_images = ProjectImage.objects.all()
        context = {
            bursaries,
            application_documents,
            ng_cdf_projects,
            citizen_report,
            report_images,
            project_images
        }
        messages.info(f'You are logged in as admin to {ng_cdf.ng_cdf_name}')
        render('dashboard/dashboard.html', context=context)
    except ObjectDoesNotExist:
        messages.error(request, f'You are not an admin')
        redirect('ng_cdf_citizen:admin_login')
