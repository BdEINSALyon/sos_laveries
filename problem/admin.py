from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = '__str__', 'type', 'serial_number', 'active', 'building'
    list_display_links = '__str__',
    search_fields = '__str__', 'serial_number'
    list_filter = 'active', 'building', 'type'

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = '__str__', 'email_resp', 'active'
    list_display_links = '__str__',
    search_fields = '__str__', 'email_resp'
    list_filter = 'active',

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = '__str__', 'machine', 'first_name', 'last_name', 'insa_email', 'count_same_email', 'get_state'
    list_display_links = '__str__',
    search_fields = '__str__', 'insa_email', 'first_name', 'last_name', 'phone_number', 'room'
    list_filter = 'state', 'machine', 'problem_type'