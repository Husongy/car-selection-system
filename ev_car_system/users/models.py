from django.db import models
from django.contrib.auth.models import User  # 导入Django自带的User模型
from django.utils import timezone

# 用户扩展信息模型（与Django自带User一对一关联）
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="关联用户")
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="昵称")
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")  # 11位手机号
    avatar = models.URLField(blank=True, null=True, verbose_name="头像链接")  # 存储头像图片的URL
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    def __str__(self):
        return self.user.username  # 显示用户名

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"