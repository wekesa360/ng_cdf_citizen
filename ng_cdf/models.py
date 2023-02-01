from django.db import models
import uuid
from accounts.models import Location, County
from accounts.models import UserProfile

class NGCDF(models.Model):
    ng_cdf_id = models.CharField(max_length=100)
    ng_cdf_name = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ng_cdf_id
    
    class Meta:
        db_table = 'ng_cdfs'


class NGCDFAdmin(models.Model):
    administrator = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    ng_cdf = models.ForeignKey(NGCDF, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ng_cdf.ng_cdf_id
    
    class Meta:
        db_table = 'ng_cdf_admins'


class NGCDFProjects(models.Model):
    CHOICES_STATUS = (
        ('', 'Select'),
        ('on-track', 'On Track'),
        ('warned', 'Warned'),
        ('issue', 'Issue'),
        ('planned', 'Planned'),
        ('postponed', 'Postponed'),
        ('completed', 'Completed')
    )

    ng_cdf = models.ForeignKey(NGCDF, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=256)
    project_id = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=CHOICES_STATUS)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    writeup_document = models.FileField(upload_to='/projects/documents/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.project_name
    
    class Meta:
        db_table = 'ng_cdf_projects'

class Bursary(models.Model):
    ng_cdf = models.ForeignKey(NGCDF, on_delete=models.CASCADE)
    bursary_id = models.CharField(max_length=256)
    bursary_type = models.CharField(max_length=256) # high school, university, form 1 intake
    bursary_name = models.CharField(max_length=256)
    deadline_of_application = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.bursary_name
    
    class Meta:
        db_table = 'bursaries'


class ApplicationDocument(models.Model):
    record_id = models.CharField(default=uuid.uuid4(), max_length=256)
    national_id = models.FileField(upload_to='/uploads/bursaries/application_documents/', null=False)
    fathers_id = models.FileField(upload_to='/uploads/bursaries/application_documents/', null=True)
    mothers_id = models.FileField(upload_to='/uploads/bursaries/application_documents/', null=True)
    institution_transcript = models.FileField(upload_to='/uploads/bursaries/application_documents/', null=True)
    calling_letter = models.FileField(upload_to='/uploads/bursaries/application_documents/', null=True)
    fee_structure  = models.FileField(upload_to='/uploads/bursaries/application_documents/', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        self.record_id
    
    class Meta:
        db_table = 'bursary_application_documents'


class BursaryApplication (models.Model):
    CHOICES_STATUS = (
        ('', 'Select'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interviewed'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    )
    applicant = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    bursary = models.ForeignKey(Bursary, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    application_documents = models.ForeignKey(ApplicationDocument, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=256)
    application_date = models.DateField()
    status = models.CharField(max_length=80, choices=CHOICES_STATUS)
    institution_location = models.ForeignKey(County, on_delete=models.DO_NOTHING)
    application_uid = models.CharField(max_length=256, default=uuid.uuid4())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.application_uid
    

    class Meta:
        db_table = 'bursary_applications'


class CitizenReport(models.Model):
    CHOICES_TYPE = (
        ('', 'Select'),
        ('complain', "Complain"),
        ('project-suggestions', 'Project suggestions'),
    )
    citizen = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=256)
    report_uid = models.CharField(default=uuid.uuid4(), max_length=256)
    project_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    report_type = models.CharField(max_length=256, choices=CHOICES_TYPE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_add_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.report_uid
    
    class Meta:
        db_table = 'citizen_reports'

class ReportImage(models.Model):
    project = models.ForeignKey(CitizenReport, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='/uploads/citizen/report/images/')
    created_at = models.DateTimeField(auto_add_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.image.url
    
    class Meta:
        db_table = 'report_images'
    
class ProjectImage(models.Model):
    project = models.ForeignKey(NGCDFProjects, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='/uploads/Ng_cdf_projects/images/')
    created_at = models.DateTimeField(auto_add_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.image.url
    
    class Meta:
        db_table = 'project_images'


