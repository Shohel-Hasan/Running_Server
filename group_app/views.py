from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from course_app.models import CourseStaff
from user_app.models import User
from .models import Group, GroupMember, GroupCriteria
from .serializers import GroupSerializer, GroupMemberSerializer, GroupCriteriaSerializer, \
    GroupMembersListSerializer, AllUserSerializer
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model


# Group ViewSet
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    def all_group_list(self, request):
        queryset = Group.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def my_group_list(self, request, user_id):
        user_ins = get_user_model().objects.filter(pk=user_id).exists()
        if user_ins:
            user = get_user_model().objects.get(pk=user_id)
            if user == request.user:
                group = Group.objects.filter(creator=user)
                if group.exists():
                    serializer = self.serializer_class(group, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "You don't have any group."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        data = request.data
        data['creator'] = request.user.id
        print("Creator: ", data)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            group = serializer.save()
            GroupMember.objects.create(group=group, member=group.creator, role='Creator')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        group = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(group)
        return Response(serializer.data)

    def update(self, request, pk):
        group = Group.objects.filter(pk=pk).exists()
        if group:
            group = Group.objects.get(pk=pk)
            if group.creator == request.user:
                data = request.data
                data['creator'] = request.user.id
                serializer = self.get_serializer(group, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You are not the creator of this group."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        queryset = self.queryset
        group = get_object_or_404(queryset, pk=pk)
        if group:
            group.delete()
            return Response({"message": "Group deleted."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def search_group(self, request):
        search_data = request.GET.get('name')
        if search_data:
            queryset = self.queryset.filter(Q(name__icontains=search_data)).distinct()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        return Response({"message": "Search not found."}, status=status.HTTP_404_NOT_FOUND)


class GroupCriteriaViewSet(viewsets.ModelViewSet):
    queryset = GroupCriteria.objects.select_related('group').all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupCriteriaSerializer

    def list(self, request, group_pk):
        group_instance = Group.objects.filter(id=group_pk).exists()
        if group_instance:
            queryset = self.queryset.filter(group=group_pk)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, group_pk):
        group_instance = Group.objects.filter(id=group_pk, creator=request.user.id).exists()
        if group_instance:
            data = request.data
            data['group'] = group_pk
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, group_pk, criteria_pk):
        # queryset = self.queryset
        group_criteria = GroupCriteria.objects.filter(pk=criteria_pk, group=group_pk).exists()
        if group_criteria:
            criteria = GroupCriteria.objects.get(pk=criteria_pk, group=group_pk)
            if criteria:
                serializer = self.serializer_class(criteria)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Criteria not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, group_pk, criteria_pk):
        group_criteria = GroupCriteria.objects.filter(pk=criteria_pk, group=group_pk).exists()
        if group_criteria:
            criteria = GroupCriteria.objects.get(pk=criteria_pk, group=group_pk)
            if criteria:
                data = request.data
                data['group'] = group_pk
                serializer = self.get_serializer(criteria, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Criteria not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, group_pk, criteria_pk):
        group_criteria = GroupCriteria.objects.filter(pk=criteria_pk, group=group_pk).exists()
        if group_criteria:
            criteria = GroupCriteria.objects.get(pk=criteria_pk, group=group_pk)
            if criteria:
                criteria.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "Criteria not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)


# Group member ViewSet
class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.select_related('group', 'member').all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupMemberSerializer

    def list(self, request, group_id):
        group_instance = Group.objects.filter(id=group_id, creator=request.user.id).exists()
        if group_instance:
            queryset = self.queryset.filter(group=group_id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Group member not found here."}, status=status.HTTP_404_NOT_FOUND)

    # user join into the group as a member
    def create(self, request, group_id):
        data = request.data
        member = request.data['member']
        data['group'] = group_id
        serializer = self.get_serializer(data=data)
        member_instance = GroupMember.objects.filter(group=data['group'], member=member).exists()
        if not member_instance:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'you are already a member in this group.'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, group_id, member_id):
        group_member = GroupMember.objects.filter(group=group_id, member_id=member_id).exists()
        print(group_member)
        if group_member:
            member = GroupMember.objects.get(group=group_id, member_id=member_id)
            if member:
                serializer = self.serializer_class(member)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"message": "Member not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, group_id):
        group_instance = GroupMember.objects.filter(group=group_id).exists()
        if group_instance:
            data = request.data
            member = request.data['member']
            role = request.data['role']
            member = GroupMember.objects.filter(group=group_id, member=member)
            if member:
                member.update(role=role)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'message': 'you are not a member in this group.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'you are not a member in this group.'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, group_id, member_id):
        group_instance = GroupMember.objects.filter(group=group_id, member=member_id).exists()
        if group_instance:
            member = GroupMember.objects.get(group=group_id, member=member_id)
            if member:
                print('member: ', member)
                member.delete()
                return Response({'message': 'Member deleted from this group.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'you are not a member in this group.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'you are not a member in this group.'}, status=status.HTTP_400_BAD_REQUEST)


class GroupView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if ser.is_valid(raise_exception=True):
            self.perform_create(ser)
            group = ser.save()
            GroupMember.objects.create(group=group, member=group.creator, role='Creator')
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupMembersListView(generics.ListCreateAPIView):
    serializer_class = GroupMembersListSerializer
    # queryset = GroupMember.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroupMember.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        group_id = self.kwargs.get('group_id')
        members = queryset.filter(group_id=group_id)
        group_members = []
        for member in members:
            try:
                group_members.append({
                    "id": member.member.id,
                    "email": member.member.email,
                    "first_name": member.member.first_name,
                    "last_name": member.member.last_name,
                    "birthdate": member.member.birthdate,
                    "gender": member.member.gender,
                    "academic_discipline": member.member.academic_discipline,
                    "profession": member.member.profession,
                    "profile_pic": member.member.general_info_user.profile_pic.url
                })
            except:
                group_members.append({
                    "id": member.member.id,
                    "email": member.member.email,
                    "first_name": member.member.first_name,
                    "last_name": member.member.last_name,
                    "birthdate": member.member.birthdate,
                    "gender": member.member.gender,
                    "academic_discipline": member.member.academic_discipline,
                    "profession": member.member.profession
                })
        # serializer = GroupMembersListSerializer(members, many=True)
        # data = serializer.data
        return Response(group_members)


class NormalGroupMembersView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    # queryset = GroupMember.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            group_id = self.kwargs.get('group_id')
            course_id = self.kwargs.get('course_id')
            course_staffs = CourseStaff.objects.filter(course_id=course_id).values_list('staff_id')
            if len(search):
                return User.objects.filter(~Q(id__in=course_staffs), group_member_user__group_id=group_id).filter(Q(first_name__icontains=search) | Q(email__icontains=search))
            else:
                return User.objects.filter(~Q(id__in=course_staffs), group_member_user__group_id=group_id)
        except:

            return User.objects.filter(~Q(id__in=course_staffs), group_member_user__group_id=group_id)


class AllUserView(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAuthenticated]

    # queryset = User.objects.all()

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        try:
            search = self.request.query_params.get('search')

            if len(search):
                queryset = User.objects.filter(~Q(group_member_user__group_id=group_id), ~Q(is_superuser=True))
                data = queryset.filter(Q(first_name__icontains=search) | Q(email__icontains=search))
            else:
                queryset = User.objects.filter(~Q(group_member_user__group_id=group_id), ~Q(is_superuser=True))
                data = queryset
        except:
            queryset = User.objects.filter(~Q(group_member_user__group_id=group_id), ~Q(is_superuser=True))
            data = queryset

        # members_table = GroupMember.objects.filter(group=Group.objects.get(id=group_id)).values_list('member_id')
        # queryset = User.objects.filter(~Q(id__in=members_table))
        # queryset = User.objects.exclude(group_member_user__group_id=group_id)
        # data = queryset.filter(Q(first_name=search) | Q(email=search))
        # ser = AllUserSerializer(queryset, many=True)
        return data
