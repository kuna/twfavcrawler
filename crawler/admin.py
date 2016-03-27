from django.contrib import admin
from models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'screen_name', 'name')
    search_fields = ['screen_name', 'name']

class TaskAdmin(admin.ModelAdmin):
    list_display = ('output', 'type', 'date', 'user', 'status', 'message')
    search_fields = ['type', 'output']

class LogAdmin(admin.ModelAdmin):
    list_display = ('task', 'message')
    search_fields = ['message']

admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Log, LogAdmin)
