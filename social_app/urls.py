from django.urls import path
from social_app.views import SocialView, FollowView  # , LikedView

app_name = 'social_app'

urlpatterns = [
    path('<int:group_pk>/<int:course_pk>/comment/', SocialView.as_view({'post': 'comment'}), name='comment'),
    path('<int:group_pk>/<int:course_pk>/comment-list/', SocialView.as_view({'get': 'list'}), name='comment_list'),
    path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-detail/', SocialView.as_view({'get': 'retrieve'}),
         name='comment_detail'),
    path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-update/', SocialView.as_view({'patch': 'update'}),
         name='comment_update'),
    path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-delete/', SocialView.as_view({'delete': 'destroy'}),
         name='comment_delete'),

    # reply urls
    path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-reply/', SocialView.as_view({'post': 'reply'}),
         name='comment_reply'),
    path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-reply-update/',
         SocialView.as_view({'patch': 'reply_update'}), name='comment_reply_update'),
    # path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-reply-list/', SocialView.as_view({
    # 'get':'reply_list'}), name='comment_reply_list'),
    path('<int:group_pk>/<int:course_pk>/<int:comment_pk>/comment-reply-delete/',
         SocialView.as_view({'delete': 'reply_destroy'}), name='comment_reply_delete'),

    # follow urls
    path('create-following/', FollowView.as_view({'post': 'follow_create'}), name='follow_create'),
    path('following/<int:user_pk>/', FollowView.as_view({'get': 'following'}), name='following'),
    path('followers/<int:following_id>/', FollowView.as_view({'get': 'followers'}), name='followers'),
    path('unfollow/', FollowView.as_view({'delete': 'unfollow'}), name='unfollow'),

    # liked url path('<int:group_pk>/<int:course_pk>/like/', LikedView.as_view({'post':'like'}), name='like'),
    # path('<int:group_pk>/<int:course_pk>/<int:liked_pk>/unlike/', LikedView.as_view({'post':'unlike'}),
    # name='unlike'), path('<int:group_pk>/<int:course_pk>/like-list/', LikedView.as_view({'get':'like_list'}),
    # name='like_list'),
]
