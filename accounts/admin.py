from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.
class MysUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 
                    'date_joined', 'is_active')
    list_filter = ()
    fieldsets = ()
    filter_horizontal = ()
    ordering = ('-date_joined',)


admin.site.register(Account, MysUserAdmin)