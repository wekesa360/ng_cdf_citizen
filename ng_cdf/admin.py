from django.contrib import admin
from .models import (
    NGCDF,
    NGCDFAdmin,
    NGCDFProjects,
    Bursary,
    ApplicationDocument,
    BursaryApplication,
    CitizenReport,
    ReportImage,
    ProjectImage
)

admin.site.register(NGCDF)
admin.site.register(NGCDFAdmin)
admin.site.register(NGCDFProjects)
admin.site.register(Bursary)
admin.site.register(ApplicationDocument)
admin.site.register(BursaryApplication)
admin.site.register(CitizenReport)
admin.site.register(ReportImage)
admin.site.register(ProjectImage)