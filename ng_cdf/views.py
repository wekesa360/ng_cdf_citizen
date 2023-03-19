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
    BursaryApplication,
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


def check_if_admin(user):
    admin = User.objects.get(email=user)
    try:
        check_admin = NGCDFAdmin.objects.get(administrator=admin)
        ng_cdf = check_admin.ng_cdf
        print('**************************************************************************')
        print(ng_cdf.id)
    except ObjectDoesNotExist:
        ng_cdf = None
    return ng_cdf

def home_view(request):
    return render(request,'landing-page.html')
    
@login_required
def admin_view(request):
    user_email = request.user.email
    print(user_email)
    try:
        ng_cdf = check_if_admin(user_email)
        user = User.objects.get(email=user_email)
        try:
            bursaries = Bursary.objects.filter(ng_cdf=ng_cdf)
        except ObjectDoesNotExist:
            bursaries = None
            bursary_applications = []
        if bursaries.count() > 1:
            if bursaries != None:
                print(bursaries.id)
                for bursary in bursaries:
                    try:
                        bursary_applications.append(BursaryApplication.objects.get(bursary=bursary))
                    except ObjectDoesNotExist:
                        pass
            else:
                bursary_applications = None
        else:
            bursary_applications = bursaries
        try:
            ng_cdf_projects = NGCDFProjects.objects.get(ng_cdf=ng_cdf)
        except ObjectDoesNotExist:
            ng_cdf_projects = None
        try:
            citizen_report = CitizenReport.objects.get(ng_cdf=ng_cdf)
        except ObjectDoesNotExist:
            citizen_report = None
        context = {
            'admin': user,
            'bursaries':bursaries,
            'bursary_applications': bursary_applications,
            'ng_cdf_projects':ng_cdf_projects,
            'citizen_report':citizen_report,
        }
        messages.info(request, f'You are logged in as admin to {ng_cdf.ng_cdf_name}')
        return render(request, 'admin-account/dashboard.html', context=context)
    except ObjectDoesNotExist:
        messages.error(request, f'You are not an admin')
        return redirect('ng_cdf:home')

@login_required
def admin_reports_view(request):
    user_email = request.user.email
    ng_cdf = check_if_admin(user_email)
    if ng_cdf != None:
        citizen_reports = CitizenReport.objects.filter(ng_cdf=ng_cdf)
    else:
        citizen_reports = None 
    context = {
            'reports': citizen_reports
        }
    return render(request, 'admin-account/citizen-reports.html', context=context)
    
@login_required
def add_project_view(request):
    user_email = request.user.email
    try:
        ng_cdf = check_if_admin(user_email)
        if request.method == 'POST':
            form = NGCDFProjectsForm(request.POST)
            image_form = ProjectImageForm(request.POST, request.FILES)
            if form.is_valid() and image_form.is_valid():
                form.save()
                project = NGCDFProjects.objects.get(project_name=form.project_name)
                image_form.project = project.id
                image_form.save()
                messages.success(request, f'Project added successfully')
                redirect('ng_cdf:projects')
            else:
                messages.error(request, f'Error adding project')
                redirect('ng_cdf:projects')
        if request.method == 'GET':
            form = NGCDFProjectsForm()
            image_form = ProjectImageForm()
            context = {
                'image_form': image_form,
                'form':form
            }
            return render(request, 'admin-account/projects-form.html', context=context)
    except ObjectDoesNotExist:
        messages.error(request, 'Not an admin')
        return redirect('ng_cdf:projects')
    return redirect('ng_cdf:projects')

@login_required
def admin_projects_view(request):
    user_email = request.user.email
    ng_cdf = check_if_admin(user_email)
    if ng_cdf != None:
        projects = NGCDFProjects.objects.filter(ng_cdf=ng_cdf)
    else:
        projects = None
    context = {
        'projects':projects
    }
    return render(request, 'admin-account/projects.html', context=context)

@login_required
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
            redirect('ng_cdf:edit-project')
    if request.method == 'GET':
        form = NGCDFProjectsForm(instance=project)
        context = {
            'form':form
        }
        return render('admin-account/projects-form-edit.html', context=context)
    return redirect('ng_cdf:edit-project')

@login_required
def delete_project_view(request, id):
    project = NGCDFProjects.objects.get(id=id)
    project.delete()
    return redirect('ng_cdf:dashboard')

@login_required
def add_bursary_view(request):
    user_email = request.user.email
    ng_cdf = check_if_admin(user_email)
    if request.method == 'POST':
        form = BursaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bursary added successfully')
            redirect('ng_cdf:add-bursary')
        else:
            messages.error(request, f'Error adding bursary')
            redirect('ng_cdf:add-bursary')
    if request.method == 'GET':
        form = BursaryForm(initial={'ng_cdf': ng_cdf})
        context = {
            'form':form,
            'ng_cdf':ng_cdf
        }
        return render(request, 'admin-account/bursaries-form.html', context=context)
    return redirect('ng_cdf:add-bursary')


@login_required
def edit_bursary_view(request, bursary_id):
    bursary = Bursary.objects.get(id=bursary_id)
    ng_cdf = check_if_admin(request.user.email)
    if ng_cdf != bursary.ng_cdf:
        messages.error(request, f'You are not authorized to edit this bursary')
        return redirect('ng_cdf:dashboard')

    else:
        if request.method == 'POST':
            form = BursaryForm(request.POST, instance=bursary)
            if form.is_valid():
                form.save()
                messages.success(request, f'Bursary updated successfully')
                redirect('ng_cdf:dashboard')
            else:
                messages.error(request, f'Error updating bursary')
                redirect('ng_cdf:edit-bursary')
        if request.method == 'GET':
            form = BursaryForm(instance=bursary)
            context = {
                'form':form
            }
            return render(request, 'admin-account/bursaries-form-edit.html', context=context)
        return redirect('ng_cdf:edit-bursary')

@login_required
def delete_bursary_view(request, id):
    user = request.user.username
    ng_cdf = check_if_admin(user)
    if ng_cdf is not None:
        bursary = Bursary.objects.get(id=id, ng_cdf=ng_cdf)
        bursary.delete()
        return redirect('ng_cdf:dashboard')

def projects_view(request):
    if request.method == 'GET':
        projects = NGCDFProjects.objects.all()
        project_images = ProjectImage.objects.all()
        context = {
            'projects':projects,
            'project_images': project_images
            }
        return render('ng_cdf/projects.html', context=context)
    else:
        redirect('nd_cdf:home')
    return redirect ('ng_cdf:projects')

@login_required
def admin_bursaries_view(request, status):
    if request.method == 'GET':
        if status == 'available':
            bursaries = Bursary.objects.filter(available=True)
        elif status == 'closed':
            bursaries = Bursary.objects.filter(available=False)
        context = {
            'bursaries':bursaries
        }
        return render(request, 'admin-account/bursaries.html', context=context)
    return redirect('ng_cdf:bursaries')


def bursaries_view(request, status):
    if request.method == 'GET':
        if status == 'available':
            bursaries = Bursary.objects.filter(available=True)
        elif status == 'closed':
            bursaries = Bursary.objects.filter(available=False)
        context = {
            'bursaries':bursaries
        }
        return render(request, 'bursaries.html', context=context)
    return redirect('ng_cdf:bursaries')

@login_required
def apply_bursary_view(request, bursary_id):
    user = request.user.username
    user = User.objects.get(email=user)
    if request.method == 'POST':
        bursary = Bursary.objects.get(bursary_id=bursary_id)
        form = BursaryApplicationForm(request.POST)
        form.bursary = bursary.id
        document_form = ApplicationDocumentForm(request.POST, request.FILES)
        document_form.bursary = bursary.id
        if form.is_valid() and document_form.is_valid():
            form.save()
            document_form.save()
            messages.success(request, f'Bursary application submitted successfully')
            redirect('ng_cdf:bursaries')
        else:
            messages.error(request, f'Error submitting bursary application')
            redirect('ng_cdf:apply_bursary')
    if request.method == 'GET':
        form = BursaryApplicationForm()
        document_form = ApplicationDocumentForm()
        bursary = Bursary.objects.get(bursary_id=bursary_id)
        context = {
            'form':form,
            'bursary':bursary,
            'document_form':document_form
        }
        return render('ng_cdf/apply-bursary.html', context=context)
    return redirect('ng_cdf:apply-bursary')

@login_required
def citizen_report_view(request):
    user = request.user.username
    user = User.objects.get(email=user)
    if request.method == 'POST':
        form = CitizenReportForm(request.POST)
        image_form = ReportImageForm(request.POST, request.FILES)
        form.citizen = user 
        if form.is_valid() and image_form.is_valid():
            form.save()
            project_name = form.clean_data.get('project_name')
            report = CitizenReport.objects.get(project_name=project_name)
            image_form.project = report.id
            image_form.save()
            messages.success(request, f'Report submitted successfully')
            redirect('ng_cdf:projects')
        else:
            messages.error(request, f'Error submitting report')
            redirect('ng_cdf:citizen-report')
    if request.method == 'GET':
        form = CitizenReportForm()
        image_form = ReportImageForm()
        context = {
            'form':form,
            'image_form':image_form
        }
        return render('ng_cdf/citizen-report.html', context=context)
    return redirect('ng_cdf:citizen-report')

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

@login_required
def delete_report_view(request, id):
    user_email = request.user.username
    user = User.objects.get(email=user_email)
    report = CitizenReport.objects.get(id=id, citizen=user)
    report.delete()
    return redirect('ng_cdf:dashboard')

