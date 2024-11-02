from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_first_name', 'get_last_name', 'get_email', 'department_display', 'manager_display')

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'  

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email' 

    def department_display(self, obj):
        return dict(UserProfile.DEPARTMENT_CHOICES).get(obj.department)
    department_display.short_description = 'Department' 
    def manager_display(self, obj):
        return obj.manager.username if obj.manager else None
    manager_display.short_description = 'Manager'
admin.site.register(UserProfile, UserProfileAdmin)