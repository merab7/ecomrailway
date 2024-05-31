from django.contrib import admin
from .models import  Profile
from django.contrib.auth.models import User


admin.site.register(Profile)


#profile and user info

class ProfileInline(admin.StackedInline):
    model = Profile


#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name',
'email', 'password1', 'password2', 'city', 'address', 'phone', 'zipcode'  ]
    inlines = [ProfileInline]

#unregister
admin.site.unregister(User)

#re_register
admin.site.register(User, UserAdmin)