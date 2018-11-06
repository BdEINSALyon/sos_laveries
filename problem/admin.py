from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Building, Machine, Ticket)
class Admin(admin.ModelAdmin):
    pass
