from rest_framework import serializers

from user_app.models import User
from user_app.serializers import UserSerializer
from user_app import models as user_model
from .models import Group, GroupMember, GroupCriteria
from django.contrib.auth import get_user_model


class AllUserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.URLField(source='general_info_user.profile_pic')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'profile_pic')


class GroupSerializer(serializers.ModelSerializer):
    academic_discipline = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id', 'creator', 'name', 'cover_pic', 'profile_pic', 'about', 'is_verified', 'academic_discipline', 'email',
            'first_name', 'profession')
        extra_kwargs = {
            'creator': {'read_only': True}
        }

    def get_academic_discipline(self, obj):
        user = obj.creator.academic_discipline
        return user

    def get_email(self, obj):
        user = obj.creator.email
        return user

    def get_first_name(self, obj):
        user = obj.creator.first_name
        return user

    def get_profession(self, obj):
        user = obj.creator.profession
        return user


class GroupCriteriaSerializer(serializers.ModelSerializer):
    group_info = serializers.SerializerMethodField()

    class Meta:
        model = GroupCriteria
        fields = "__all__"

    def get_group_info(self, obj):
        group = obj.group
        return GroupInfoSerializer(group).data


class GroupInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'cover_pic', 'profile_pic', 'about', 'is_verified',)


class GroupMemberSerializer(serializers.ModelSerializer):
    group_info = serializers.SerializerMethodField()
    academic_discipline = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()

    class Meta:
        model = GroupMember
        fields = (
            'id', 'group', 'member', 'role', 'group_info', 'academic_discipline', 'email', 'first_name', 'profession')

    def get_group_info(self, obj):
        group = obj.group
        return GroupInfoSerializer(group).data

    def get_academic_discipline(self, obj):
        member = obj.member.academic_discipline
        return member

    def get_email(self, obj):
        member = obj.member.email
        return member

    def get_first_name(self, obj):
        member = obj.member.first_name
        return member

    def get_profession(self, obj):
        member = obj.member.profession
        return member


class GroupMembersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'
