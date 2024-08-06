from django.contrib import admin
from hospitalapp.models import Patient,Appointment,Member

# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Member)
