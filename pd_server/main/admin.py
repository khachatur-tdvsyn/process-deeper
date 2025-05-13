from django.contrib import admin
from .models import Computer, ProcessStat, Process, ComputerStat
# Register your models here.

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('os', 'hostname', 'ram', 'network_interfaces')

@admin.register(ComputerStat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('record_time', 'computer__hostname', 'cpu_load', 'ram_load', 'network_load')

#admin.site.register(Computer, ComputerAdmin)
admin.site.register([Process, ProcessStat])