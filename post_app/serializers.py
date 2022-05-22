from rest_framework import serializers
from post_app.models import ThoughtPost, SummeryPost, CommentModel
from user_app.models import User


class ThoughtPostSerializer(serializers.ModelSerializer):
    user_cover_pic = serializers.SerializerMethodField()
    user_profile_pic = serializers.SerializerMethodField()
    user_first_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    group_cover_pic = serializers.SerializerMethodField()
    group_profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = ThoughtPost
        fields = (
            'id',
            'user',
            'group',
            'description',
            'user_cover_pic',
            'created_date',
            'user_profile_pic',
            'user_first_name',
            'group_name',
            'group_cover_pic',
            'group_profile_pic',
        )

    def get_user_cover_pic(self, obj):
        try:
            cover_pic = obj.user.general_info_user.cover_pic.url
            return cover_pic
        except:
            cover_pic = ''
            return cover_pic

    def get_user_profile_pic(self, obj):
        try:
            profile_pic = obj.user.general_info_user.profile_pic.url
            return profile_pic
        except:
            profile_pic = ''
            return profile_pic

    def get_user_first_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return ''

    def get_group_name(self, obj):
        try:
            return obj.group.name
        except:
            return ''

    def get_group_cover_pic(self, obj):
        try:
            cover_pic = obj.group.cover_pic.url
            return cover_pic
        except:
            cover_pic = ''
            return cover_pic

    def get_group_profile_pic(self, obj):
        try:
            profile_pic = obj.group.profile_pic.url
            return profile_pic
        except:
            profile_pic = ''
            return profile_pic


class SummeryPostSerializer(serializers.ModelSerializer):
    user_cover_pic = serializers.SerializerMethodField()
    user_profile_pic = serializers.SerializerMethodField()
    user_first_name = serializers.SerializerMethodField()
    group_name = serializers.SerializerMethodField()
    group_cover_pic = serializers.SerializerMethodField()
    group_profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = SummeryPost
        fields = (
            'id',
            'user',
            'group',
            'title_of_research_article',
            'objective_of_the_study',
            'theoritical_Background',
            'research_gap',
            'uniqueness_of_the_study',
            'data_source_sample_information',
            'research_methodology',
            'result_discussion',
            'validity_reliability_of_finding',
            'usefulness_of_the_finding',
            'reference',
            'annex',
            'file1',
            'file2',
            'keyword',
            'created_date',
            'user_cover_pic',
            'user_profile_pic',
            'user_first_name',
            'group_name',
            'group_cover_pic',
            'group_profile_pic',
        )

    def get_user_cover_pic(self, obj):
        try:
            cover_pic = obj.user.general_info_user.cover_pic.url
            return cover_pic
        except:
            cover_pic = ''
            return cover_pic

    def get_user_profile_pic(self, obj):
        try:
            profile_pic = obj.user.general_info_user.profile_pic.url
            return profile_pic
        except:
            profile_pic = ''
            return profile_pic

    def get_user_first_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return ''

    def get_group_name(self, obj):
        try:
            return obj.group.name
        except:
            return ''

    def get_group_cover_pic(self, obj):
        try:
            cover_pic = obj.group.cover_pic.url
            return cover_pic
        except:
            cover_pic = ''
            return cover_pic

    def get_group_profile_pic(self, obj):
        try:
            profile_pic = obj.group.profile_pic.url
            return profile_pic
        except:
            profile_pic = ''
            return profile_pic


class CommentUserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.CharField(source='general_info_user.profile_pic')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'profile_pic']


class CommentSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer(read_only=True)

    class Meta:
        model = CommentModel
        fields = '__all__'

        extra_kwargs = {
            'thought_post': {'read_only': True},
            'summary_post': {'read_only': True},
            'parent': {'read_only': True}
        }
