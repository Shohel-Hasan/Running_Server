import random
from cgitb import reset
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView

from post_app.models import ThoughtPost, SummeryPost, CommentModel
from post_app.serializers import ThoughtPostSerializer, SummeryPostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from group_app.models import Group


# Create your views here.

class ThoughtPostViewset(viewsets.ModelViewSet):
    """ThoughtPost for user and group"""
    queryset = ThoughtPost.objects.all()
    serializer_class = ThoughtPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def all_thought_of_user(self, request, user_id):
        thought = ThoughtPost.objects.select_related('user', 'group').filter(user=user_id)
        serializer = self.serializer_class(thought, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def all_thought_of_group(self, request, group_id):
        summery = ThoughtPost.objects.select_related('user', 'group').filter(group=group_id)
        serializer = self.serializer_class(summery, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def user_thought_create(self, request, user_id):
        user_instance = get_user_model().objects.filter(id=user_id).exists()
        if user_instance:
            user = get_user_model().objects.get(id=user_id)
            if user and user == request.user:
                data = request.data
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "User does not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User does not found"}, status.HTTP_404_NOT_FOUND)

    def group_thought_create(self, request, group_id):
        group_instance = Group.objects.filter(id=group_id).exists()
        if group_instance:
            group = Group.objects.get(id=group_id)
            if group:
                data = request.data
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Group does not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Group does not found"}, status.HTTP_404_NOT_FOUND)

    def user_thought_single(self, request, user_id, thought_id):
        thought_instance = ThoughtPost.objects.filter(user=user_id, id=thought_id).exists()
        if thought_instance:
            thought = ThoughtPost.objects.get(user=user_id, id=thought_id)
            serializer = self.serializer_class(thought)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "ThoughtPost does not found"}, status.HTTP_404_NOT_FOUND)

    def group_thought_single(self, request, group_id, thought_id):
        group_instance = ThoughtPost.objects.filter(group=group_id, id=thought_id).exists()
        if group_instance:
            thought = ThoughtPost.objects.get(group=group_id, id=thought_id)
            serializer = self.serializer_class(thought)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "ThoughtPost does not found"}, status.HTTP_404_NOT_FOUND)

    def user_thought_single_update(self, request, user_id, thought_id, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        thought_instance = ThoughtPost.objects.filter(user=user_id, id=thought_id).exists()
        if thought_instance:
            thought = ThoughtPost.objects.get(user=user_id, id=thought_id)
            if thought and thought.user == request.user:
                serializer = self.serializer_class(thought, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "ThoughtPost not found or you are not this thought user"},
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "ThoughtPost does not found"}, status.HTTP_404_NOT_FOUND)

    def group_thought_single_update(self, request, group_id, thought_id, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        thought_instance = ThoughtPost.objects.filter(group=group_id, id=thought_id).exists()
        if thought_instance:
            thought = ThoughtPost.objects.get(group=group_id, id=thought_id)
            if thought:
                serializer = self.serializer_class(thought, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "ThoughtPost not found"}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "ThoughtPost does not found"}, status.HTTP_404_NOT_FOUND)

    def user_thought_single_delete(self, request, user_id, thought_id):
        thought_instance = ThoughtPost.objects.filter(user=user_id, id=thought_id).exists()
        if thought_instance:
            thought = ThoughtPost.objects.get(user=user_id, id=thought_id)
            if thought and thought.user == request.user:
                thought.delete()
                return Response({"message": "This thoughtpost is deleted successfully"}, status.HTTP_204_NO_CONTENT)
            return Response({"message": "Thought Post not Found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Thought Post does not match"}, status.HTTP_404_NOT_FOUND)

    def group_thought_single_delete(self, request, group_id, thought_id):
        thought_instance = ThoughtPost.objects.filter(group=group_id, id=thought_id).exists()
        if thought_instance:
            thought = ThoughtPost.objects.get(group=group_id, id=thought_id)
            if thought:
                thought.delete()
                return Response({"message": "This thoughtpost is deleted successfully"}, status.HTTP_204_NO_CONTENT)
            return Response({"message": "Thought Post not Found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Thought Post does not match"}, status.HTTP_404_NOT_FOUND)


class SummeryPostViewset(viewsets.ModelViewSet):
    """SummeryPost for user and group"""
    queryset = SummeryPost.objects.all()
    serializer_class = SummeryPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def all_summery_of_user(self, request, user_id):
        summery = SummeryPost.objects.select_related('user', 'group').filter(user=user_id)
        serializer = self.serializer_class(summery, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def all_summery_of_group(self, request, group_id):
        summery = SummeryPost.objects.select_related('user', 'group').filter(group=group_id)
        serializer = self.serializer_class(summery, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def user_summery_create(self, request, user_id):
        user_instance = get_user_model().objects.filter(id=user_id).exists()
        if user_instance:
            user = get_user_model().objects.get(id=user_id)
            if user and user == request.user:
                data = request.data
                # data['user'] = user.id
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "User does not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User does not found"}, status.HTTP_404_NOT_FOUND)

    def group_summery_create(self, request, group_id):
        group_instance = Group.objects.filter(id=group_id).exists()
        if group_instance:
            group = Group.objects.get(id=group_id)
            if group:
                data = request.data
                # data['group'] = group.id
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Group does not found"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Group does not found"}, status.HTTP_404_NOT_FOUND)

    def user_summery_single(self, request, user_id, summery_id):
        summery_instance = SummeryPost.objects.filter(user=user_id, id=summery_id).exists()
        if summery_instance:
            summery = SummeryPost.objects.get(user=user_id, id=summery_id)
            serializer = self.serializer_class(summery)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "SummeryPost does not found"}, status.HTTP_404_NOT_FOUND)

    def group_summery_single(self, request, group_id, summery_id):
        summery_instance = SummeryPost.objects.filter(group=group_id, id=summery_id).exists()
        if summery_instance:
            summery = SummeryPost.objects.get(group=group_id, id=summery_id)
            serializer = self.serializer_class(summery)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "SummeryPost does not found"}, status.HTTP_404_NOT_FOUND)

    def user_summery_single_update(self, request, user_id, summery_id, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        summery_instance = SummeryPost.objects.filter(user=user_id, id=summery_id).exists()
        if summery_instance:
            summery = SummeryPost.objects.get(user=user_id, id=summery_id)
            if summery and summery.user == request.user:
                serializer = self.serializer_class(summery, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "SummeryPost not found or you are not this thought user"},
                                status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "SummeryPost does not found"}, status.HTTP_404_NOT_FOUND)

    def group_summery_single_update(self, request, group_id, summery_id, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        summery_instance = SummeryPost.objects.filter(group=group_id, id=summery_id).exists()
        if summery_instance:
            summery = SummeryPost.objects.get(group=group_id, id=summery_id)
            if summery:
                serializer = self.serializer_class(summery, data=request.data, partial=partial)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "SummeryPost not found"}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "SummeryPost does not found"}, status.HTTP_404_NOT_FOUND)

    def user_summery_single_delete(self, request, user_id, summery_id):
        summery_instance = SummeryPost.objects.filter(user=user_id, id=summery_id).exists()
        print(summery_instance, "summary ins")
        if summery_instance:
            summery = SummeryPost.objects.get(user=user_id, id=summery_id)
            if summery and summery.user == request.user:
                summery.delete()
                return Response({"message": "This summerypost is deleted successfully"}, status.HTTP_204_NO_CONTENT)
            return Response({"message": "Summery Post not Found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Summery Post does not match"}, status.HTTP_404_NOT_FOUND)

    def group_summery_single_delete(self, request, group_id, summery_id):
        summery_instance = SummeryPost.objects.filter(group=group_id, id=summery_id).exists()
        print("summary instance: ", summery_instance)
        if summery_instance:
            summery = SummeryPost.objects.get(group=group_id, id=summery_id)
            if summery:
                summery.delete()
                return Response({"message": "This summerypost is deleted successfully"}, status.HTTP_204_NO_CONTENT)
            return Response({"message": "Summery Post not Found"}, status.HTTP_404_NOT_FOUND)
        return Response({"message": "Summery Post does not match"}, status.HTTP_404_NOT_FOUND)


class GroupPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # queryset = ThoughtPost.objects.all()

    def get(self, request, *args, **kwargs):
        thought = ThoughtPost.objects.filter(group__isnull=False)
        summery = SummeryPost.objects.filter(group__isnull=False)
        data = []

        thought_data = ThoughtPostSerializer(thought, many=True)
        summery_data = SummeryPostSerializer(summery, many=True)
        combine = thought_data.data + summery_data.data

        data.append(combine)
        random.shuffle(data[0])
        if data[0]:
            return Response(data[0])
        else:
            return Response({
                "message": "No Data Found"
            })


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # queryset = ThoughtPost.objects.all()

    def get(self, request, *args, **kwargs):
        thought = ThoughtPost.objects.all()
        summery = SummeryPost.objects.all()
        data = []

        thought_data = ThoughtPostSerializer(thought, many=True)
        summery_data = SummeryPostSerializer(summery, many=True)
        combine = thought_data.data + summery_data.data

        data.append(combine)
        random.shuffle(data[0])
        if data[0]:
            return Response(data[0])
        else:
            return Response({
                "message": "No Data Found"
            })


class UserPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        thought = ThoughtPost.objects.filter(user_id=self.kwargs.get('user_id'))
        summery = SummeryPost.objects.filter(user_id=self.kwargs.get('user_id'))
        data = {
            "thought": [],
            "summery": []
        }

        thought_data = ThoughtPostSerializer(thought, many=True)
        summery_data = SummeryPostSerializer(summery, many=True)
        for td in thought_data.data:
            data['thought'].append(td)
        for sd in summery_data.data:
            data['summery'].append(sd)

        if data:
            return Response(data)
        else:
            return Response({
                "message": "No Data Found"
            })


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CommentModel.objects.all()

    def perform_create(self, serializer):
        post_type = self.kwargs.get('type')
        post_id = self.kwargs.get('post_id')
        if post_type == 'thought':
            serializer.save(thought_post=ThoughtPost.objects.get(id=post_id), user=self.request.user)
        elif post_type == 'summary':
            serializer.save(summary_post=SummeryPost.objects.get(id=post_id), user=self.request.user)

    def get_queryset(self):
        post_type = self.kwargs.get('type')
        post_id = self.kwargs.get('post_id')
        if post_type == 'thought':
            queryset = CommentModel.objects.filter(thought_post_id=post_id)
        elif post_type == 'summary':
            queryset = CommentModel.objects.filter(summary_post_id=post_id)

        return queryset


class SinglePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            post_type = self.kwargs.get('type')
            post_id = self.kwargs.get('post_id')
            if post_type == 'thought':
                thought = ThoughtPost.objects.get(id=post_id)
                data = ThoughtPostSerializer(thought)
            if post_type == 'summary':
                summery = SummeryPost.objects.get(id=post_id)
                data = SummeryPostSerializer(summery)
            return Response(data.data)
        except:
            return Response({
                "message": "No Data Found"
            })
