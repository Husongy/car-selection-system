"""
将用户设置为超级用户
"""
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
django.setup()

from django.contrib.auth.models import User

# 修改这里的用户名
username = 'hsy'

# 如果需要重置密码，取消下面这行的注释并设置新密码
# new_password = 'your_new_password'
new_password = None

try:
    user = User.objects.get(username=username)
    user.is_superuser = True
    user.is_staff = True
    
    # 如果设置了新密码，则重置密码
    if new_password:
        user.set_password(new_password)
        print(f"🔑 密码已重置为: {new_password}")
    
    user.save()
    print(f"✅ 用户 '{username}' 已设置为超级用户！")
    print(f"📝 现在可以用这个账号登录 Admin 后台了")
except User.DoesNotExist:
    print(f"❌ 用户 '{username}' 不存在！")
    print("请先注册该用户，或者创建新的超级用户：")
    print("  python manage.py createsuperuser")
