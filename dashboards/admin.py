
from django.contrib import admin
from .models import Dashboard
@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('area','nombre','fuente','esprivado')
    search_fields = ('area','nombre','fuente')
    list_filter = ('area','esprivado')
