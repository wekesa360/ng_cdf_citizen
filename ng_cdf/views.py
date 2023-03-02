from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
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
            'bursaries':bursaries,
            'application_documents':application_documents,
            'ng_cdf_projects':ng_cdf_projects,
            'citizen_report':citizen_report,
            'report_images':report_images,
            'project_images':project_images
        }
        messages.info(f'You are logged in as admin to {ng_cdf.ng_cdf_name}')
        render('dashboard/dashboard.html', context=context)
    except ObjectDoesNotExist:
        messages.error(request, f'You are not an admin')
        redirect('ng_cdf_citizen:admin_login')

def projects_view(request):
    if request.method == 'GET':
        projects = NGCDFProjects.objects.all()
        project_images = ProjectImage.objects.all()
        context = {
            'projects':projects,
            'project_images': project_images
            }
        return render('ng_cdf/projects.html', context=context)
    return redirect ('ng_cdf:projects')

def add_project_view(request):
    if request.method == 'POST':
        form = NGCDFProjectsForm(request.POST)
        image_form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            form.save()
            image_form.save()
            messages.success(request, f'Project added successfully')
            redirect('ng_cdf:projects')
        else:
            messages.error(request, f'Error adding project')
            redirect('ng_cdf:add_project')
    else:
        form = NGCDFProjectsForm()
        context = {
            'form':form
        }
        return render('ng_cdf/add_project.html', context=context)
    if request.method == 'GET':
        form = NGCDFProjectsForm()
        context = {
            'form':form
        }
        return render('ng_cdf/add_project.html', context=context)
    return redirect('ng_cdf:add_project')

def bursaries_view(request):
    if request.method == 'GET':
        bursaries = Bursary.objects.all()
        context = {
            'bursaries':bursaries
        }
        return render('ng_cdf/bursaries.html', context=context)
    return redirect('ng_cdf:bursaries')

def add_bursary_view(request):
    if request.method == 'POST':
        form = BursaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bursary added successfully')
            redirect('ng_cdf:bursaries')
        else:
            messages.error(request, f'Error adding bursary')
            redirect('ng_cdf:add_bursary')
    else:
        form = BursaryForm()
        context = {
            'form':form
        }
        return render('ng_cdf/add_bursary.html', context=context)
    if request.method == 'GET':
        form = BursaryForm()
        context = {
            'form':form
        }
        return render('ng_cdf/add_bursary.html', context=context)
    return redirect('ng_cdf:add_bursary')

def apply_bursary_view(request):
    if request.method == 'POST':
        form = BursaryApplicationForm(request.POST)
        document_form = ApplicationDocumentForm(request.POST, request.FILES)
        if form.is_valid() and document_form.is_valid():
            form.save()
            document_form.save()
            messages.success(request, f'Bursary application submitted successfully')
            redirect('ng_cdf:bursaries')
        else:
            messages.error(request, f'Error submitting bursary application')
            redirect('ng_cdf:apply_bursary')
    else:
        form = BursaryApplicationForm()
        document_form = ApplicationDocumentForm()
        context = {
            'form':form,
            'document_form':document_form
        }
        return render('ng_cdf/apply_bursary.html', context=context)
    if request.method == 'GET':
        form = BursaryApplicationForm()
        document_form = ApplicationDocumentForm()
        context = {
            'form':form,
            'document_form':document_form
        }
        return render('ng_cdf/apply_bursary.html', context=context)
    return redirect('ng_cdf:apply_bursary')

def citizen_report_view(request):
    if request.method == 'POST':
        form = CitizenReportForm(request.POST)
        image_form = ReportImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            form.save()
            image_form.save()
            messages.success(request, f'Report submitted successfully')
            redirect('ng_cdf:projects')
        else:
            messages.error(request, f'Error submitting report')
            redirect('ng_cdf:citizen_report')
    else:
        form = CitizenReportForm()
        image_form = ReportImageForm()
        context = {
            'form':form,
            'image_form':image_form
        }
        return render('ng_cdf/citizen_report.html', context=context)
    if request.method == 'GET':
        form = CitizenReportForm()
        image_form = ReportImageForm()
        context = {
            'form':form,
            'image_form':image_form
        }
        return render('ng_cdf/citizen_report.html', context=context)
    return redirect('ng_cdf:citizen_report')

def delete_project_view(request, id):
    project = NGCDFProjects.objects.get(id=id)
    project.delete()
    return redirect('ng_cdf:dashboard')

def delete_bursary_view(request, id):
    bursary = Bursary.objects.get(id=id)
    bursary.delete()
    return redirect('ng_cdf:dashboard')

def delete_report_view(request, id):
    report = CitizenReport.objects.get(id=id)
    report.delete()
    return redirect('ng_cdf:dashboard')

def edit_project_view(request, id):
    project = NGCDFProjects.objects.get(id=id)
    if request.method == 'POST':
        form = NGCDFProjectsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project updated successfully')
            redirect('ng_cdf:dashboard')
        else:
            messages.error(request, f'Error updating project')
            redirect('ng_cdf:edit_project')
    else:
        form = NGCDFProjectsForm(instance=project)
        context = {
            'form':form
        }
        return render('ng_cdf/edit_project.html', context=context)
    if request.method == 'GET':
        form = NGCDFProjectsForm(instance=project)
        context = {
            'form':form
        }
        return render('ng_cdf/edit_project.html', context=context)
    return redirect('ng_cdf:edit_project')

def edit_bursary_view(request, id):
    bursary = Bursary.objects.get(id=id)
    if request.method == 'POST':
        form = BursaryForm(request.POST, instance=bursary)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bursary updated successfully')
            redirect('ng_cdf:dashboard')
        else:
            messages.error(request, f'Error updating bursary')
            redirect('ng_cdf:edit_bursary')
    else:
        form = BursaryForm(instance=bursary)
        context = {
            'form':form
        }
        return render('ng_cdf/edit_bursary.html', context=context)
    if request.method == 'GET':
        form = BursaryForm(instance=bursary)
        context = {
            'form':form
        }
        return render('ng_cdf/edit_bursary.html', context=context)
    return redirect('ng_cdf:edit_bursary')

def edit_report_view(request, id):
    report = CitizenReport.objects.get(id=id)
    if request.method == 'POST':
        form = CitizenReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, f'report updated successfully')
            redirect('ng_cdf:edit_report')
        else:
            messages.error(request, f'Error updating report')
            redirect('ng_cdf:edit_report')
    else:
        form = CitizenReportForm(instance=report)
        context = {
            'form' : form
        }
        return render('ng_cdf/edit_report.html', context=context)
    return redirect('ng_cdf:edit_report')
