from django.contrib import admin
from .models import Group, GroupCriteria, GroupMember


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['creator', 'name', 'cover_pic', 'profile_pic', 'about', 'is_verified']


@admin.register(GroupCriteria)
class GroupCriteriaAdmin(admin.ModelAdmin):
    list_display = ['group', 'criteria_title', 'criteria_detail']


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['group', 'member', 'role']
