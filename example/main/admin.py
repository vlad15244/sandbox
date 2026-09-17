from django.contrib import admin

# Register your models here.
from .models import MyModels

admin.site.register(MyModels)