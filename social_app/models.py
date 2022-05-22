from django.db import models
from core_app.models import BaseModel
from group_app.models import Group
from django.conf import settings
from course_app.models import Course
from django.contrib.auth.models import User
from user_app.models import User
from django.db.models.signals import post_save, post_delete
from django.urls import reverse


# Create your models here.
class CommentModel(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_comment_user')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.course}'

    def children(self):
        return CommentModel.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class FollowingModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_id'], name='unique_following')
        ]

    def __str__(self):
        return f'{self.user} follows {self.following_id}'

# class Liked(BaseModel):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     likes = models.ManyToManyField(User, related_name='course_like')

#     def __str__(self):
#         return '{} : {}'.format(self.user, self.course)

#     def get_likes(self):
#         return self.likes.count()
