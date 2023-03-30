from django.db import models
from django.urls import reverse
import uuid
from accounts.models import Location, County
from django.core.validators import FileExtensionValidator
from accounts.models import UserProfile

class NGCDF(models.Model):
    ng_cdf_id = models.CharField(max_length=100)
    ng_cdf_name = models.CharField(max_length=256)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.ng_cdf_name
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
    writeup_document = models.FileField(upload_to='projects/documents/', null=True,
                                        validators=[FileExtensionValidator(['pdf'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.project_name
    
    def get_absolute_url(self):
        return reverse("ng_cdf:project-detail", kwargs={"project_id": self.pk})
    
    def get_images(self):
        return ProjectImage.objects.filter(project=self)
    
    class Meta:
        db_table = 'ng_cdf_projects'

class ProjectImage(models.Model):
    project = models.ForeignKey(NGCDFProjects, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/Ng_cdf_projects/images/',
                              validators=[FileExtensionValidator(['jpg','png','jpeg'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.image.url
    
    class Meta:
        db_table = 'project_images'

class Bursary(models.Model):
    ng_cdf = models.ForeignKey(NGCDF, on_delete=models.CASCADE)
    bursary_id = models.CharField(max_length=256)
    application_documents = models.CharField(max_length=256, default='None')
    available = models.BooleanField(default=True)
    bursary_type = models.CharField(max_length=256) # high school, university, form 1 intake
    bursary_name = models.CharField(max_length=256)
    deadline_of_application = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.bursary_name
    
    def get_absolute_url(self):
        return reverse("ng_cdf:bursary-detail", kwargs={"bursary_id": self.pk})
    
    class Meta:
        db_table = 'bursaries'


class BursaryApplication(models.Model):
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
    institution_name = models.CharField(max_length=256)
    application_date = models.DateField()
    status = models.CharField(max_length=80, choices=CHOICES_STATUS, default='pending')
    institution_location = models.ForeignKey(County, on_delete=models.DO_NOTHING)
    application_uid = models.CharField(max_length=256, default=uuid.uuid4())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.application_uid
    
    def delete_url(self):
        return reverse("ng_cdf:delete-application", kwargs={"id": self.pk})

    class Meta:
        db_table = 'bursary_applications'

class ApplicationDocument(models.Model):
    application = models.ForeignKey(BursaryApplication, on_delete=models.CASCADE)
    record_id = models.CharField(default=uuid.uuid4(), max_length=256)
    national_id = models.FileField(upload_to='uploads/bursaries/application_documents/', null=False,
                                   validators=[FileExtensionValidator(['pdf','jpg','png','jpeg'])])
    fathers_id = models.FileField(upload_to='uploads/bursaries/application_documents/', null=True,
                                   validators=[FileExtensionValidator(['pdf','jpg','png','jpeg'])])
    mothers_id = models.FileField(upload_to='uploads/bursaries/application_documents/', null=True,
                                   validators=[FileExtensionValidator(['pdf','jpg','png','jpeg'])])
    institution_transcript = models.FileField(upload_to='uploads/bursaries/application_documents/', null=True,
                                   validators=[FileExtensionValidator(['pdf',])])
    calling_letter = models.FileField(upload_to='uploads/bursaries/application_documents/', null=True,
                                   validators=[FileExtensionValidator(['pdf'])])
    fee_structure  = models.FileField(upload_to='uploads/bursaries/application_documents/', null=False,
                                   validators=[FileExtensionValidator(['pdf',])])
    other = models.FileField(upload_to='uploads/bursaries/application_documents/', null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.record_id
    
    class Meta:
        db_table = 'bursary_application_documents'





class CitizenReport(models.Model):
    CHOICES_TYPE = (
        ('', 'Select'),
        ('complain', "Complain"),
        ('project-suggestions', 'Project suggestions'),
    )
    citizen = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ng_cdf = models.ForeignKey(NGCDF, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=256)
    report_uid = models.CharField(default=uuid.uuid4(), max_length=256)
    project_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    report_type = models.CharField(max_length=256, choices=CHOICES_TYPE)
    description = models.TextField()
    report_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.report_uid
    
    class Meta:
        db_table = 'citizen_reports'

class ReportImage(models.Model):
    report = models.ForeignKey(CitizenReport, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/citizen/report/images/',
                              validators=[FileExtensionValidator(['jpg','png','jpeg'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.image.url
    
    class Meta:
        db_table = 'report_images'