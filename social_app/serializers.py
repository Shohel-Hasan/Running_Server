from rest_framework import serializers
from .models import CommentModel, FollowingModel


class CommentChildSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=CommentModel.objects.all(), source='parent.id')
    first_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()


    class Meta:
        model = CommentModel
        fields = ('first_name', 'profile_image', 'content', 'id','parent_id')


    def get_first_name(self, obj):
        return obj.user.first_name

    def create(self, validated_data):
        subject = parent.objects.create(parent=validated_data['parent']['id'], content=validated_data['content'])
        return subject

    def get_profile_image(self, obj):
        try:
            return obj.user.usergeneralinfo.profile_pic.url
        except:
            return None


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = ('first_name','profile_image', 'id','content', 'parent', 'reply_count', 'replies')

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_profile_image(self, obj):
        try:
            return obj.user.usergeneralinfo.profile_pic.url
        except:
            return None


class FollwingSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = FollowingModel
        fields = ('id', 'following_id', 'profile_pic', 'first_name')
    
    def get_profile_pic(self, obj):
        try:
            return obj.following.usergeneralinfo.profile_pic.url
        except:
            return None
    
    def get_first_name(self, obj):
        return obj.following_id.first_name

class FollowersSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    class Meta:
        model = FollowingModel
        fields = ('id', 'user', 'first_name', 'profile_pic')

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_profile_pic(self, obj):
        try:
            return obj.user.usergeneralinfo.profile_pic.url
        except:
            return None


# original
# class LikedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Liked 
#         fields = "__all__"

    # def get_liked_count(self, obj):
    #     return obj.liked.count()

    # def get_liked_user(self, obj):
    #     return obj.liked.all()

