from django.urls import path
from post_app import views

app_name ='post_app'

# Thought Post Action
user_thought_create = views.ThoughtPostViewset.as_view({
    'post': 'user_thought_create'
})

group_thought_create = views.ThoughtPostViewset.as_view({
    'post': 'group_thought_create'
})
thought_list = views.ThoughtPostViewset.as_view({
    'get': 'list'
})

user_thought_single = views.ThoughtPostViewset.as_view({
    'get': 'user_thought_single',
    'patch': 'user_thought_single_update',
    'delete': 'user_thought_single_delete'
})

group_thought_single = views.ThoughtPostViewset.as_view({
    'get': 'group_thought_single',
    'patch': 'group_thought_single_update',
    'delete': 'group_thought_single_delete'
})

all_thought_of_user = views.ThoughtPostViewset.as_view({
    'get': 'all_thought_of_user'
})
all_thought_of_group = views.ThoughtPostViewset.as_view({
    'get': 'all_thought_of_group'
})

# Summery Post Action
user_summery_create = views.SummeryPostViewset.as_view({
    'post': 'user_summery_create'
})

group_summery_create = views.SummeryPostViewset.as_view({
    'post': 'group_summery_create'
})
summery_list = views.SummeryPostViewset.as_view({
    'get': 'list'
})

user_summery_single = views.SummeryPostViewset.as_view({
    'get': 'user_summery_single',
    'patch': 'user_summery_single_update',
    'delete': 'user_summery_single_delete'
})

group_summery_single = views.SummeryPostViewset.as_view({
    'get': 'group_summery_single',
    'patch': 'group_summery_single_update',
    'delete': 'group_summery_single_delete'
})


all_summery_of_user = views.SummeryPostViewset.as_view({
    'get': 'all_summery_of_user'
})
all_summery_of_group = views.SummeryPostViewset.as_view({
    'get': 'all_summery_of_group'
})

urlpatterns = [
    # ThoughtPost
    # User Thought 
    path(
        '<int:user_id>/user-thought-create/',
        user_thought_create,
        name='user-thought-create'
    ),
    path(
        '<int:user_id>/user-thought/<int:thought_id>/',
        user_thought_single,
        name='user-thought-single'
    ),
    # Group Thought
    path(
        '<int:group_id>/group-thought-create/',
        group_thought_create,
        name='group-thought-create'
    ),
    path(
        '<int:group_id>/group-thought/<int:thought_id>/',
        group_thought_single,
        name='group-thought-single'
    ),

    # All Posts
    path('group-post/all/', views.GroupPostView.as_view()),
    path('all/', views.PostView.as_view()),
    path('user-posts/<int:user_id>/', views.UserPostView.as_view()),

    path(
        'thoughtpost/all/',
        thought_list,
        name='thought-list'
    ),
    path(
        '<int:user_id>/user-thought-all/',
        all_thought_of_user,
        name='all-thought-of-user'
    ),
    path(
        '<int:group_id>/group-thought-all/',
        all_thought_of_group,
        name='all-thought-of-group'
    ),
    # SummeryPost
    # User Summery
    path(
        '<int:user_id>/user-summery-create/',
        user_summery_create,
        name='user-summery-create'
    ),
    path(
        '<int:user_id>/user-summery/<int:summery_id>/',
        user_summery_single,
        name='user-summery-single'
    ),
    # Group Summery
    path(
        '<int:group_id>/group-summery-create/',
        group_summery_create,
        name='group-summery-create'
    ),
    path(
        '<int:group_id>/group-summery/<int:summery_id>/',
        group_summery_single,
        name='group-summery-single'
    ),

    # All Summery
    path(
        'summerypost/all/',
        summery_list,
        name='summery-list'
    ),
    path(
        '<int:user_id>/user-summery-all/',
        all_summery_of_user,
        name='all-summery-of-user'
    ),
    path(
        '<int:group_id>/group-summery-all/',
        all_summery_of_group,
        name='all-summery-of-group'
    ),
    path('comment/<str:type>/<int:post_id>/', views.CommentView.as_view()),
    path('post/<str:type>/<int:post_id>/', views.SinglePostView.as_view()),

]
