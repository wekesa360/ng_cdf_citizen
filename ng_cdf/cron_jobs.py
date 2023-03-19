from datetime import datetime
from .models import Bursary

def check_bursary_deadline():
    bursaries = Bursary.objects.all()
    for bursary in bursaries:
        if bursary.deadline_of_application < datetime.now():
            bursary.available = False
            bursary.save()