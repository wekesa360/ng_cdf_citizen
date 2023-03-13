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

class NGCDFProjectsForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = NGCDFProjects
        fields = ('ng_cdf', 'project_name', 'project_id', 'description', 'status', 'location', 'writeup_document')


class BursaryForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = Bursary
        fields = ('ng_cdf', 'bursary_id', 'bursary_type', 'bursary_name', 'deadline_of_application', 'description',)
    
class ApplicationDocumentForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = ApplicationDocument
        fields = ('record_id', 'national_id', 'fathers_id', 'mothers_id', 'institution_transcript', 'calling_letter', 'fee_structure',)
    
class BursaryApplicationForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = BursaryApplication
        fields = ('applicant', 'bursary', 'date_of_birth', 'application_documents', 'institution_name','application_date', 'status',)

class CitizenReportForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = CitizenReport
        fields = ('citizen', 'report_type', 'project_name','report_uid','project_location','description',)
    
class ReportImageForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = ReportImage
        fields = ('report', 'image',)


class ProjectImageForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = ProjectImage
        fields = ('project', 'image',)

