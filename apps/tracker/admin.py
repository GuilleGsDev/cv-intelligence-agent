from django.contrib import admin
from apps.tracker.models import JobApplication

# Registramos el modelo para que podamos verlo en el panel de Django más adelante
admin.site.register(JobApplication)
