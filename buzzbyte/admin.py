from django.contrib import admin
from .models import Blog,User,Comment
from django.contrib.auth.admin import UserAdmin

admin.site.register(Blog)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
# Register your models here.
