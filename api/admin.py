from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from api.forms import MyUserForm
from api.models import MyUser, Wishes, Friends, WishTarget


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    add_form = MyUserForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'full_name')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'full_name')

@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user")


admin.site.register(Wishes)
admin.site.register(WishTarget)