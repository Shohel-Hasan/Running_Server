from django.urls import path
from group_app.views import GroupViewSet, GroupMemberViewSet, GroupCriteriaViewSet, \
    GroupMembersListView, GroupView, AllUserView, NormalGroupMembersView

app_name = 'group_app'

urlpatterns = [
    # Group url here.
    path(
         '<int:user_id>/my-groups/', 
         GroupViewSet.as_view({'get': 'my_group_list'}), 
         name='my_group_list'
         ),

    path(
         'all-groups/', 
         GroupViewSet.as_view({'get': 'all_group_list'}), 
         name='group_list'
         ),
    path('<int:group_id>/all-users/', AllUserView.as_view()),
         
    path(
         'create/', 
         GroupView.as_view(),
         name='group_create'
         ),

    path(
         '<int:pk>/group-detail/', 
         GroupViewSet.as_view({'get': 'retrieve'}), 
         name='group_retrieve'
         ),

    path(
         '<int:pk>/group-update/',
          GroupViewSet.as_view({'patch': 'update'}), 
          name='group_update'
          ),

    path(
         '<int:pk>/group-delete/', 
         GroupViewSet.as_view({'delete': 'destroy'}), 
         name='group_destroy'
         ),
         
    path(
         'search/', 
         GroupViewSet.as_view({'get': 'search_group'}), 
         name='search_group'
         ),


    # GroupCriteria url here.
    path(
         '<int:group_pk>/all-criteria/', 
         GroupCriteriaViewSet.as_view({'get': 'list'}), 
         name='all_group_criteria'
         ),

    path(
         '<int:group_pk>/add-criteria/', 
         GroupCriteriaViewSet.as_view({'post': 'create'}),
         name='group_criteria_create'
         ),

    path(
         '<int:group_pk>/<int:criteria_pk>/detail/', 
         GroupCriteriaViewSet.as_view({'get': 'retrieve'}),
         name='group_criteria_detail'
         ),

    path(
         '<int:group_pk>/<int:criteria_pk>/update/', 
         GroupCriteriaViewSet.as_view({'patch': 'update'}),
         name='group_criteria_update'
         ),

    path(
         '<int:group_pk>/<int:criteria_pk>/delete/', 
         GroupCriteriaViewSet.as_view({'delete': 'destroy'}),
         name='group_criteria_delete'
         ),

    # GroupMember url here.
    path('<int:group_id>/members/', GroupMembersListView.as_view()),
    path('<int:group_id>/<int:course_id>/members/', NormalGroupMembersView.as_view()),
    path(
         '<int:group_id>/all-members/',
         GroupMemberViewSet.as_view({'get': 'list'}), 
         name='group_member_list'
         ),

    path(
         '<int:group_id>/member-add/', 
         GroupMemberViewSet.as_view({'post': 'create'}), 
         name='group_member_create'
         ),

    path(
         '<int:group_id>/<int:member_id>/member-detail/', 
         GroupMemberViewSet.as_view({'get': 'retrieve'}),
         name='group_member_retrieve'
         ),

    path(
         '<int:group_id>/role-update/', 
         GroupMemberViewSet.as_view({'patch': 'update'}), 
         name='group_member_update'
         ),

    path(
         '<int:group_id>/<int:member_id>/remove/', 
         GroupMemberViewSet.as_view({'delete': 'destroy'}),
         name='group_member_destroy'
         ),
]
