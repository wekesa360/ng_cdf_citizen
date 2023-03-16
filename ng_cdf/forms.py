from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Location
from .models import (
    NGCDF,
    NGCDFProjects,
    Bursary,
    ApplicationDocument,
    BursaryApplication,
    CitizenReport,
    ReportImage,
    ProjectImage,
    
)

User = get_user_model


class CreateNGCDFForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    forms.ModelChoiceField(queryset=Location.objects.all())
    class Meta:
            model = NGCDF
            fields = ('ng_cdf_id', 'ng_cdf_name', 'location',)
            widgets = {
                'location': forms.Select(attrs={'class': 'form-control'}),
                'ng_cdf_id': forms.TextInput(attrs={'class': 'form-control'}),
                'ng_cdf_name': forms.TextInput(attrs={'class': 'form-control'}),
            }

class NGCDFProjectsForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = NGCDFProjects
        fields = ('ng_cdf', 'project_name', 'project_id', 'description', 'status', 'location', 'writeup_document')
        widgets = {
            'ng_cdf': forms.Select(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'writeup_document': forms.FileInput(attrs={'class': 'form-control'}),
        }


class BursaryForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = Bursary
        fields = ('ng_cdf', 'bursary_id', 'bursary_type', 'bursary_name', 'deadline_of_application', 'description',)
        widgets = {
            'ng_cdf': forms.Select(attrs={'class': 'form-control'}),
            'bursary_id': forms.TextInput(attrs={'class': 'form-control'}),
            'bursary_type': forms.Select(attrs={'class': 'form-control'}),
            'bursary_name': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline_of_application': forms.DateInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
class ApplicationDocumentForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = ApplicationDocument
        fields = ('record_id', 'national_id', 'fathers_id', 'mothers_id', 'institution_transcript', 'calling_letter', 'fee_structure',)
        widgets = {
            'record_id': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.FileInput(attrs={'class': 'form-control'}),
            'fathers_id': forms.FileInput(attrs={'class': 'form-control'}),
            'mothers_id': forms.FileInput(attrs={'class': 'form-control'}),
            'institution_transcript': forms.FileInput(attrs={'class': 'form-control'}),
            'calling_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'fee_structure': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
class BursaryApplicationForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = BursaryApplication
        fields = ('applicant', 'bursary', 'date_of_birth', 'application_documents', 'institution_name','application_date', 'status',)
        widgets = {
            'applicant': forms.Select(attrs={'class': 'form-control'}),
            'bursary': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'application_documents': forms.Select(attrs={'class': 'form-control'}),
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'application_date': forms.DateInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class CitizenReportForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = CitizenReport
        fields = ('citizen', 'report_type', 'project_name','report_uid','project_location','description',)
        widgets = {
            'citizen': forms.Select(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),   
            'report_uid': forms.TextInput(attrs={'class': 'form-control'}),
            'project_location': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
class ReportImageForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = ReportImage
        fields = ('report', 'image',)
        widgets = {
            'report': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProjectImageForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = ProjectImage
        fields = ('project', 'image',)
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

