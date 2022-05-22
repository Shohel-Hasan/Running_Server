import os
from django.db import models

from core_app.models import BaseModel
from user_app.models import User
from django.dispatch import receiver
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete


# Create your models here.
class Group(BaseModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_creator')
    name = models.CharField(max_length=100, null=True, blank=True)
    cover_pic = models.FileField(upload_to='group_cover_pic', null=True, blank=True)
    profile_pic = models.FileField(upload_to='group_profile_pic', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class GroupCriteria(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    criteria_title = models.CharField(max_length=100, null=True, blank=True)
    criteria_detail = models.TextField(null=True, blank=True)


class GroupMember(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_member_group')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_member_user')
    role = models.CharField(max_length=100)
