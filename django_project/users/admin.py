from django.contrib import admin
from .models import Account, MyAccountManager, Profile
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'data_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'data_joined', 'last_login')

    # required by UserAdmin, set to nothing 
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)



