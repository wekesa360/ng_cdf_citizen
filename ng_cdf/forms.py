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
            'ng_cdf': forms.TextInput(attrs={'class': 'form-control', 'value': '{{ng_cdf.id}}', 'disabled': 'true'}),
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
            'bursary_id': forms.TextInput(attrs={'class': 'form-control'}),
            'bursary_type': forms.TextInput(attrs={'class': 'form-control'}),
            'bursary_name': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline_of_application': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
class ApplicationDocumentForm(forms.Form):
    other = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    application = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    national_id = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    fathers_id = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    mothers_id = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    institution_transcript = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    calling_letter = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    fee_structure = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    def save(self):
        document = ApplicationDocument()
        document.other = self.cleaned_data['other']
        document.national_id = self.cleaned_data['national_id']
        bursary_application = BursaryApplication.objects.get(id=self.cleaned_data['application'])
        document.application = bursary_application
        document.fathers_id = self.cleaned_data['fathers_id']
        document.mothers_id = self.cleaned_data['mothers_id']
        document.institution_transcript = self.cleaned_data['institution_transcript']
        document.calling_letter = self.cleaned_data['calling_letter']
        document.fee_structure = self.cleaned_data['fee_structure']
        document.save()
        return document
    
class BursaryApplicationForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = BursaryApplication
        fields = ('applicant', 'bursary', 'date_of_birth', 'institution_name','application_date', 'institution_location')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'application_documents': forms.Select(attrs={'class': 'form-control'}),
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'institution_location': forms.Select(attrs={'class': 'form-control'}),
            'application_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class CitizenReportForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """

    class Meta:
        model = CitizenReport
        fields = ('ng_cdf', 'report_date', 'citizen', 'report_type', 'project_name','project_location','description',)
        widgets = {
            'report_date': forms.DateInput(attrs={'class': 'form-control bg-white border-0', 'style':'height: 55px;', 'type': 'date'}),
            'report_type': forms.Select(attrs={'class': 'form-control bg-white border-0', 'style':'height: 55px;',}),
            'project_name': forms.TextInput(attrs={'class': 'form-control bg-white border-0', 'style':'height: 55px;', }),   
            'ng_cdf': forms.Select(attrs={'class': 'form-control bg-white border-0', 'style':'height: 55px;', 'placeholder': 'NG CDF'}),
            'project_location': forms.Select(attrs={'class': 'form-control bg-white border-0', 'style':'height: 55px;',}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-white border-0', }),
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
            'image': forms.FileInput(attrs={'class': 'form-control', 'multiple': True}),
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

