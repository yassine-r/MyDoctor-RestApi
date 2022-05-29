from django.contrib import admin
from .models import Patient, Facility, MyUser

# Register your models here.
admin.site.register(Patient)
admin.site.register(Facility)
admin.site.register(MyUser)
