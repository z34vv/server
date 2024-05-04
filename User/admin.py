from django.contrib import admin
from .models import User, Bag, Item


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id',
        'username',
        'email',
        'phone',
        'age',
        'gender',
    ]

    list_filter = [
        'gender',
        'is_active',
        'is_staff',
        'is_superuser',
    ]


class BagAdmin(admin.ModelAdmin):
    list_display = [
        'bag_id', 'user', 'sapphires'
    ]


class UserAdminSite(admin.AdminSite):
    site_header = "USER MANAGEMENT"


custom_admin_site = UserAdminSite()


admin.site.register(User, UserAdmin)
admin.site.register(Bag, BagAdmin)
