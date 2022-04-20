from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Post

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # Only display the "username" field
    fields = ["username", 'email']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.unregister(Group)
