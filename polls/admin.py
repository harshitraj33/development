from django.contrib import admin

# Register your models here.
from .models import users, FormModel, LoginUser, SignupUser
admin.site.register(users)

admin.site.register(FormModel)
admin.site.register(LoginUser)
admin.site.register(SignupUser)