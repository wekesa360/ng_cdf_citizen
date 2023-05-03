from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import uuid
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
        print(ng_cdf.id)
    except ObjectDoesNotExist:
        ng_cdf = None
    return ng_cdf

def constituencies_view(request):
    return render(request, 'ng_cdf/constituencies.html')

def faqs_view(request):
    return render(request, 'ng_cdf/faqs.html')

def home_view(request):
    return render(request,'ng_cdf/index.html')

def about_view(request):
    return render(request, 'ng_cdf/about.html')


@login_required
def admin_view(request):
    user_email = request.user.email
    try:
        ng_cdf = check_if_admin(user_email)
        if ng_cdf != None:
            user = User.objects.get(email=user_email)
            try:
                bursaries = Bursary.objects.filter(ng_cdf=ng_cdf)
                bursary_applications = []
            except ObjectDoesNotExist:
                bursaries = None
                bursary_applications = []
            if bursaries.count() > 1:
                if bursaries != None:
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
                ng_cdf_projects = NGCDFProjects.objects.filter(ng_cdf=ng_cdf)
            except ObjectDoesNotExist:
                ng_cdf_projects = None
            try:
                citizen_report = CitizenReport.objects.filter(ng_cdf=ng_cdf)
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
            return render(request, 'admin-dashboard/dashboard.html', context=context)
        else:
            messages.error(request, f'You are not an admin')
            return redirect('ng_cdf:home')
    except ObjectDoesNotExist:
        messages.error(request, f'You are not an admin')
        return redirect('ng_cdf:home')


@login_required
def admin_reports_view(request):
    user_email = request.user.email
    ng_cdf = check_if_admin(user_email)
    if ng_cdf != None:
        reports = CitizenReport.objects.filter(ng_cdf=ng_cdf)
        
    else:
        reports = None 
    context = {
            'reports': reports
        }
    return render(request, 'admin-dashboard/reports.html', context=context)


@login_required
def admin_report_details_view(request, report_id):
    report = CitizenReport.objects.get(id=report_id)
    images = ReportImage.objects.filter(report=report)
    context = {
        'report': report,
        'report_images': images,
    }
    return render(request, 'admin-dashboard/report-detail.html', context=context)



@login_required
def upload_project_images_view(request, project_id):
    project = NGCDFProjects.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectImageForm(request.FILES, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Images saved successfully")
            return redirect("ng_cdf:projects")
    form = ProjectImageForm(initial={'project': project})
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'admin-account/project_image_upload.html')



@login_required
def add_project_view(request):
    user_email = request.user.email
    try:
        ng_cdf = check_if_admin(user_email)
        if request.method == 'POST':
            form = NGCDFProjectsForm(request.POST)
            image_form = ProjectImageForm(request.POST, request.FILES)
            if form.is_valid():
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
            return render(request, 'admin-dashboard/add-projects.html', context=context)
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
    return render(request, 'admin-dashboard/projects.html', context=context)



@login_required
def edit_project_view(request, project_id):
    project = NGCDFProjects.objects.get(id=project_id)
    if request.method == 'POST':
        form = NGCDFProjectsForm(request.POST, instance=project)
        import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            messages.success(request, f'Project updated successfully')
            redirect('ng_cdf:dashboard')
        else:
            messages.error(request, f'Error updating project')
            return redirect('ng_cdf:edit-project', project_id=project_id)
    if request.method == 'GET':
        form = NGCDFProjectsForm(instance=project)
        context = {
            'form':form
        }
        return render(request,'admin-dashboard/edit-project.html', context=context)
    return redirect('ng_cdf:edit-project', project_id=project_id)


@login_required
def delete_project_view(request, project_id):
    project = NGCDFProjects.objects.get(id=project_id)
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
        return render(request, 'admin-dashboard/add-bursary.html', context=context)
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
                redirect(reverse('ng_cdf:edit-bursary', args=[bursary_id]))
            else:
                messages.error(request, f'Error updating bursary')
                redirect(reverse('ng_cdf:edit-bursary', args=[bursary_id]))
        form = BursaryForm(instance=bursary, initial={'ng_cdf': ng_cdf})
        context = {
            'form':form,
            'ng_cdf': ng_cdf
        }
        return render(request, 'admin-dashboard/edit-bursary.html', context=context)
    return redirect(reverse('ng_cdf:edit-bursary', args=[bursary_id]))


@login_required
def delete_bursary_view(request, bursary_id):
    user = request.user.email
    ng_cdf = check_if_admin(user)
    if ng_cdf is not None:
        bursary = Bursary.objects.get(id=bursary_id, ng_cdf=ng_cdf)
        bursary.delete()
        return redirect('ng_cdf:bursaries')

def projects_view(request):
    if request.method == 'GET':
        projects = NGCDFProjects.objects.all()
        project_images = ProjectImage.objects.all()
        context = {
            'projects':projects,
            'project_images': project_images
            }
        return render(request, 'ng_cdf/projects-view.html', context=context)
    else:
        redirect('nd_cdf:home')
    return redirect ('ng_cdf:projects')

def project_detail_view(request, project_id):
    if request.method == 'GET':
        project = NGCDFProjects.objects.get(id=project_id)
        project_images = ProjectImage.objects.filter(project=project.id)
        context = {
            'project':project,
            'project_images': project_images
            }
        return render(request, 'ng_cdf/project-detail.html', context=context)
    else:
        redirect('nd_cdf:home')
    return redirect ('ng_cdf:project-detail')


@login_required
def admin_bursaries_view(request):
    if request.method == 'GET':
        bursaries = Bursary.objects.filter(ng_cdf=check_if_admin(request.user.email))
        context = {
            'bursaries':bursaries
        }
        return render(request, 'admin-dashboard/bursaries.html', context=context)
    return redirect('ng_cdf:bursaries')


def bursaries_view(request):
    if request.method == 'GET':
        bursaries = Bursary.objects.filter(available=True)
        context = {
            'bursaries':bursaries
        }
        return render(request, 'ng_cdf/bursaries-view.html', context=context)
    return redirect('ng_cdf:citizen-bursaries')



@login_required
def bursary_applications_view(request):
    user = request.user.email
    user = User.objects.get(email=user)
    applications = BursaryApplication.objects.filter(applicant=user.id)
    if request.method == 'GET':
        context = {
            'applications': applications
        }
        return render(request, 'ng_cdf/applications-view.html', context=context)
    return redirect(reverse('ng_cdf:bursary-applications'))

def update_application_status(request, id):
    application = get_object_or_404(BursaryApplication, pk=id)
    
    new_status = request.POST.get('status')
    if new_status not in dict(BursaryApplication.CHOICES_STATUS).keys():
        raise ValueError('Invalid status')
    
    application.update_application_status(new_status)
    
    return redirect('ng_cdf:admin-bursary-applications')


@login_required
def view_application_view(request, application_id):
    application = BursaryApplication.objects.get(id=application_id)
    application_documents = ApplicationDocument.objects.filter(application=application.id)
    if request.method == 'GET':
        context = {
            'application': application,
            'application_documents': application_documents
        }
        return render(request, 'admin-dashboard/view-application.html', context=context)
    return redirect(reverse('ng_cdf:view-applications', args=[application_id]))


@login_required
def admin_bursary_applications_view(request):
    user = request.user.email
    user = User.objects.get(email=user)
    applications = BursaryApplication.objects.filter(applicant=user.id)
    if request.method == 'GET':
        context = {
            'applications': applications
        }
        return render(request, 'admin-dashboard/bursary-applications.html', context=context)
    return redirect(reverse('ng_cdf:bursary-applications'))



@login_required
def upload_bursary_documents_view(request, application_id):
    user = request.user.email
    user = User.objects.get(email=user)
    application = BursaryApplication.objects.get(id=application_id)
    if request.method == 'POST':
        form = ApplicationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.application = application_id
            form.save()
            messages.success(request, f'Document uploaded successfully')
            redirect('ng_cdf:bursaries-list')
        else:
            messages.error(request, f'Error uploading document')
            redirect(reverse('ng_cdf:upload-documents', args=[application_id]))
    if request.method == 'GET':
        form = ApplicationDocumentForm(initial={'application': application_id})
        context = {
            'document_form':form,
            'bursary': application.bursary,
            'application': application
        }
        return render(request, 'ng_cdf/bursary-application-documents.html', context=context)
    return redirect('ng_cdf:bursaries-list')


@login_required
def apply_bursary_view(request, bursary_id):
    user = request.user.email
    user = User.objects.get(email=user)
    if request.method == 'POST':
        bursary = Bursary.objects.get(id=bursary_id)
        form = BursaryApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            bursary_application = BursaryApplication.objects.filter(applicant=user.id, bursary=bursary_id).latest('created_at').id
            return redirect(reverse('ng_cdf:upload-documents', args=[bursary_application]))
        else:
            messages.error(request, f'Error submitting bursary application')
            redirect(reverse('ng_cdf:apply-bursary', args=[bursary_id]))
    if request.method == 'GET':
        form = BursaryApplicationForm(initial={'bursary': bursary_id, 'applicant': user.id})
        bursary = Bursary.objects.get(id=bursary_id)
        context = {
            'form':form,
            'user': user,
            'bursary':bursary,
        }
        return render(request, 'ng_cdf/bursary-application-form.html', context=context)
    return redirect(reverse('ng_cdf:apply-bursary', args=[bursary_id]))


@login_required
def citizen_report_view(request):
    user = request.user.email
    user = User.objects.get(email=user)
    if request.method == 'POST':
        form = CitizenReportForm(request.POST)
        if form.is_valid():
            form.save()
            project_name = form.cleaned_data.get('project_name')
            report_cdf = form.cleaned_data.get('ng_cdf')
            report = CitizenReport.objects.filter(project_name=project_name, citizen=user.id).filter(ng_cdf=report_cdf).latest('created_at')
            image_form = ReportImageForm(request.POST, request.FILES)

            if image_form.is_valid():
                image_form.cleaned_data['report'] = report.id
                image_form.save()
                messages.success(request, f'Report submitted successfully')
                return redirect('ng_cdf:citizen-report')
            else:
                messages.error(request, f'Error uploading images')
                return redirect('ng_cdf:citizen-report')
        else:
            messages.error(request, f'Error submitting report')
            redirect('ng_cdf:citizen-report')
    if request.method == 'GET':
        form = CitizenReportForm(initial={'citizen': user.id})
        image_form = ReportImageForm()
        context = {
            'form':form,
            'user': user,
            'image_form':image_form
        }
        return render(request, 'ng_cdf/project-suggestion.html', context=context)
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
def delete_application_view(request, id):
    user_email = request.user.email
    user = User.objects.get(email=user_email)
    application = BursaryApplication.objects.get(id=id, applicant=user)
    application.delete()
    return redirect('ng_cdf:bursary-applications')



def check_if_admin(user):
    admin = User.objects.get(email=user)
    try:
        check_admin = NGCDFAdmin.objects.get(administrator=admin)
        ng_cdf = check_admin.ng_cdf
        print(ng_cdf.id)
    except ObjectDoesNotExist:
        ng_cdf = None
    return ng_cdf


@login_required
def upload_project_images_view(request, project_id):
    project = NGCDFProjects.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectImageForm(request.FILES, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Images saved successfully")
            return redirect("ng_cdf:projects")
    form = ProjectImageForm(initial={'project': project})
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'admin-account/project_image_upload.html')


@login_required
def admin_bursary_detail_view(request, bursary_id):
    """view a single bursary"""
    bursary = Bursary.objects.get(id=bursary_id)
    context = {
        'bursary': bursary
    }
    return render(request, 'admin-dashboard/bursary-detail.html', context=context)


@login_required
def change_availability_view(request, bursary_id):
    """change availability of a bursary"""
    bursary = Bursary.objects.get(id=bursary_id)
    if bursary.available:
        bursary.available = False
        bursary.save()
        messages.success(request, f'Bursary is now unavailable for application')
        return redirect(reverse('ng_cdf:admin-bursary-detail', kwargs={'bursary_id': bursary.id}))
    else:
        bursary.available = True
        bursary.save()
        messages.success(request, f'Bursary is now available for application')
        return redirect(reverse('ng_cdf:admin-bursary-detail', kwargs={'bursary_id': bursary.id}))


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
        return render(request, 'admin-dashboard/add-bursary.html', context=context)
    return redirect('ng_cdf:add-bursary')


@login_required
def delete_bursary_view(request, bursary_id):
    user = request.user.email
    ng_cdf = check_if_admin(user)
    if ng_cdf is not None:
        bursary = Bursary.objects.get(id=bursary_id, ng_cdf=ng_cdf)
        bursary.delete()
        return redirect('ng_cdf:bursaries')

def projects_view(request):
    if request.method == 'GET':
        projects = NGCDFProjects.objects.all()
        project_images = ProjectImage.objects.all()
        context = {
            'projects':projects,
            'project_images': project_images
            }
        return render(request, 'ng_cdf/projects-view.html', context=context)
    else:
        redirect('nd_cdf:home')
    return redirect ('ng_cdf:projects')


@login_required
def admin_project_detail_view(request, project_id):
    if request.method == 'GET':
        project = NGCDFProjects.objects.get(id=project_id)
        project_images = ProjectImage.objects.filter(project=project.id)
        context = {
            'project':project,
            'project_images': project_images
            }
        return render(request, 'admin-dashboard/project-detail.html', context=context)
    else:
        redirect('nd_cdf:home')
    return redirect ('ng_cdf:admin-project-detail')


@login_required
def admin_bursaries_view(request):
    if request.method == 'GET':
        bursaries = Bursary.objects.filter(ng_cdf=check_if_admin(request.user.email))
        context = {
            'bursaries':bursaries
        }
        return render(request, 'admin-dashboard/bursaries.html', context=context)
    return redirect('ng_cdf:bursaries')


def admin_bursaries_list_view(request, status):
    if request.method == 'GET':
        if status == 'available':
            bursaries = Bursary.objects.filter(available=True)
        elif status == 'closed':
            bursaries = Bursary.objects.filter(available=False)
        context = {
            'bursaries':bursaries
        }
        return render(request, 'ng_cdf/bursaries-view.html', context=context)
    return redirect('ng_cdf:bursaries-list')

def bursaries_view(request):
    if request.method == 'GET':
        bursaries = Bursary.objects.filter(available=True)
        context = {
            'bursaries':bursaries
        }
        return render(request, 'ng_cdf/bursaries-view.html', context=context)
    return redirect('ng_cdf:citizen-bursaries')

def bursary_detail_view(request, bursary_id):
    if request.method == 'GET':
        bursary = Bursary.objects.get(id=bursary_id)
        context = {
            'bursary':bursary
            }
        return render(request, 'ng_cdf/bursary-detail.html', context=context)
    else:
        redirect('nd_cdf:home')
    return redirect ('ng_cdf:project-detail')


@login_required
def admin_citizen_reports_view(request):
    """admin reports view"""
    admin = request.user.email
    ng_cdf = NGCDF.objects.get(email=admin)
    if request.method == 'GET':
        reports = CitizenReport.objects.filter(ng_cdf=ng_cdf.id)
        context = {
            'reports': reports
        }
        return render(request, 'admin-dashboard/reports.html', context=context)
    return redirect('ng_cdf:admin-reports')
