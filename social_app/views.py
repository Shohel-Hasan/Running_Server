from django.shortcuts import render
from course_app.models import Course, GroupCourse
from user_app.models import User
from group_app.models import Group, GroupMember
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import CommentModel, FollowingModel
from .serializers import CommentSerializer, FollwingSerializer, FollowersSerializer
from course_app.serializers import CourseSerializer
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.db.models.functions import Coalesce
from django.db.models import Count, Sum, Value


# Create your views here.
class SocialView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Course.objects.all()
    groups = Group.objects.all()
    serializer_class = CommentSerializer
    # serializer_class2 = CommentChildSerializer

    #comment
    def comment(self, request, course_pk, group_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course = Course.objects.filter(pk=course_pk).exists()

            if course:
                course = Course.objects.get(pk=course_pk)
                data = request.data
                data['course'] = course.pk
                serializer = CommentSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(course=course, user=request.user)
                    return Response(serializer.data)
                return Response(serializer.errors)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)



    def list(self, request, course_pk, group_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course = Course.objects.filter(pk=course_pk).exists()
            if course:
                course = Course.objects.get(pk=course_pk)
                comments = CommentModel.objects.filter(course=course)
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, course_pk, group_pk, comment_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course = Course.objects.filter(pk=course_pk).exists()
            if course:
                course = Course.objects.get(pk=course_pk)
                comment = CommentModel.objects.filter(pk=comment_pk).exists()
                if comment:
                    comment = CommentModel.objects.get(pk=comment_pk)
                    serializer = CommentSerializer(comment)
                    return Response(serializer.data)
                return Response({'message': 'Comment not founded'}, status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    def update(self, request, course_pk, group_pk, comment_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course = Course.objects.filter(pk=course_pk).exists()
            if course:
                course = Course.objects.get(pk=course_pk)
                comment = CommentModel.objects.filter(pk=comment_pk).exists()
                if comment:
                    comment = CommentModel.objects.get(pk=comment_pk)
                    serializer = CommentSerializer(comment, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status.HTTP_201_CREATED)
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'Comment not founded'}, status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    def destroy(self, request, course_pk, group_pk, comment_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course = Course.objects.filter(pk=course_pk).exists()
            if course:
                course = Course.objects.get(pk=course_pk)
                comment = CommentModel.objects.filter(pk=comment_pk).exists()
                if comment:
                    comment = CommentModel.objects.get(pk=comment_pk)
                    comment.delete()
                    return Response({'message': 'Comment deleted'})
                return Response({'message': 'Comment not founded'}, status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    #reply
    def reply(self, request, course_pk, group_pk, comment_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        course_ins = Course.objects.filter(pk=course_pk).exists()
        if group_ins and course_ins:
            course = Course.objects.get(pk=course_pk)
            comment_ins = CommentModel.objects.filter(pk=comment_pk, course=course).exists()
            if comment_ins:
                comment = CommentModel.objects.get(pk=comment_pk)
                if comment:
                    data = request.data
                    
                    # data['course'] = course.pk
                    data['parent'] = comment.pk
                    serializer = CommentSerializer(data=data)
                    # serializer = CommentChildSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save(course=course, user=request.user)
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)
                return Response({'message': 'Comment not founded'}, status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group or course not founded'}, status.HTTP_404_NOT_FOUND)

    def reply_update(self, request, group_pk, course_pk, comment_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course_ins = Course.objects.filter(pk=course_pk).exists()
            if course_ins:
                course = Course.objects.get(pk=course_pk)
                comment_ins = CommentModel.objects.filter(pk=comment_pk, course=course).exists()
                if comment_ins:
                    print('comment_ins..........: ', comment_ins)
                    comment = CommentModel.objects.get(pk=comment_pk)
                    if comment:
                        print('comment..........: ', comment)
                        serializer = CommentSerializer(comment, data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data)
                        return Response(serializer.errors)
                    return Response({'message': 'Comment not founded'}, status.HTTP_404_NOT_FOUND)
                return Response({'message': 'Comment not founded'}, status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    def reply_destroy(self, request, group_pk, course_pk, comment_pk):
        group_ins = Group.objects.filter(pk=group_pk).exists()
        if group_ins:
            course_ins = Course.objects.filter(pk=course_pk).exists()
            if course_ins:
                course = Course.objects.get(pk=course_pk)
                comment_ins = CommentModel.objects.filter(pk=comment_pk, course=course).exists()
                if comment_ins:
                    comment_reply = CommentModel.objects.get(pk=comment_pk)
                    comment_reply.delete()
                    return Response({'message': 'Comment deleted'})
                return Response({'message':'Comment not founded'}, status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)


class FollowView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = FollowingModel.objects.all()

    def follow_create(self, request):
        user = User.objects.filter(pk=request.user.id).exists()
        following_id_ins = User.objects.filter(pk=request.data['following_id']).exists()
        if user and following_id_ins:
            is_following = FollowingModel.objects.filter(user=request.user.id, following_id=request.data['following_id']).exists()
            if is_following:
                return Response({'message': 'You are already following this user'}, status.HTTP_400_BAD_REQUEST)
            else:
                following_ins = User.objects.filter(pk=request.data['following_id']).get()
                FollowingModel.objects.create(user=request.user, following_id=following_ins)
                return Response({'message': 'You are following this user'}, status.HTTP_201_CREATED)
        return Response({'message': 'User not found'}, status.HTTP_404_NOT_FOUND)

    def following(self, request, user_pk):
        user = FollowingModel.objects.filter(user=user_pk)
        if user.exists():
            serializer = FollwingSerializer(user, many=True)
            print("serializer: ", serializer)
            return Response(serializer.data)
        return Response({'message': 'User not found'}, status.HTTP_404_NOT_FOUND)

    def followers(self, request, following_id):
        all_followers = FollowingModel.objects.filter(following_id=following_id)
        if all_followers.exists():
            serializer = FollowersSerializer(all_followers, many=True)
            return Response(serializer.data)
        return Response({'message': 'User not found'}, status.HTTP_404_NOT_FOUND)

    def unfollow(self, request):
        user = User.objects.filter(pk=request.user.id).exists()
        following_id_ins = User.objects.filter(pk=request.data['following_id']).exists()
        if user and following_id_ins:
            is_following = FollowingModel.objects.filter(user=request.user.id, following_id=request.data['following_id']).exists()
            if is_following:
                following_ins = User.objects.filter(pk=request.data['following_id']).get()
                FollowingModel.objects.filter(user=request.user, following_id=following_ins).delete()
                return Response({'message': 'You are unfollowing this user'}, status.HTTP_200_OK)
            else:
                return Response({'message': 'You are not following this user'}, status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found'}, status.HTTP_404_NOT_FOUND)


# #Like and Unlike
class LikedView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # queryset = Likes.objects.annotate(
    #     likes=Coalesce(Sum('likes__isLike'), Value(0)),
    #     unlikes=Coalesce(Count('likes')-Sum('likes__isLike'), Value(0))
    # )


#before
        # def like(self, request, group_pk, course_pk):
        # group_ins = Group.objects.filter(pk=group_pk).exists()
        # if group_ins:
        #     course_ins = Course.objects.filter(pk=course_pk).exists()
        #     if course_ins:
        #         course = Course.objects.get(pk=course_pk)
        #         already_liked = Liked.objects.filter(user=request.user, course=course)
        #         if not already_liked:
        #             course_liked = Liked(course=course, user=request.user)
        #             serializer = LikedSerializer(course_liked, data=request.data)
        #             if serializer.is_valid():
        #                 serializer.save()
        #                 return Response(serializer.data)
        #             return Response(serializer.errors)
        #         return Response({'message': 'Already liked'}, status.HTTP_400_BAD_REQUEST)
        #     return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
        # else:
        #     return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    # def unlike(self, request, group_pk, course_pk, liked_pk):
    #     group_ins = Group.objects.filter(pk=group_pk).exists()
    #     if group_ins:
    #         course_ins = Course.objects.filter(pk=course_pk).exists()
    #         if course_ins:
    #             course = Course.objects.get(pk=course_pk)
    #             already_liked = Liked.objects.filter(user=request.user, course=course, pk=liked_pk).exists()
    #             if already_liked:
    #                 liked = Liked.objects.get(pk=liked_pk)
    #                 liked.delete()
    #                 return Response({'message': 'Unliked'})
    #             return Response({'message': 'Not liked'}, status.HTTP_400_BAD_REQUEST)
    #         return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response({'message': 'Group not founded'}, status.HTTP_404_NOT_FOUND)

    # def like_list(self, request, group_pk, course_pk):
    #     group_ins = Group.objects.filter(pk=group_pk).exists()
    #     if group_ins:
    #         course_ins = Course.objects.filter(pk=course_pk).exists()
    #         if course_ins:
    #             course = Course.objects.get(pk=course_pk)
    #             if course:
    #                 liked = Liked.objects.filter(course=course)
    #                 serializer = LikedSerializer(liked, many=True)
    #                 return Response(serializer.data)
    #             return Response({'message': 'course not founded here'}, status.HTTP_404_NOT_FOUND)
    #         return Response({'message': 'Course not founded'}, status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response({'message': 'Group is not founded'}, status.HTTP_404_NOT_FOUND)


