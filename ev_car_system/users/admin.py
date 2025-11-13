
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile
from django.contrib import admin

# 扩展User的admin显示
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "用户扩展信息"

# 重写UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# 先注销默认的User admin，再注册自定义的
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

# 扩展User的admin显示
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "用户扩展信息"

# 重写UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# 先注销默认的User admin，再注册自定义的
admin.site.unregister(User)
admin.site.register(User, UserAdmin)