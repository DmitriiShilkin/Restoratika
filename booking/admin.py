from django.contrib import admin

from .models import Application, Hall, Table

# Register your models here.
admin.site.register(Hall)
admin.site.register(Table)
admin.site.register(Application)
