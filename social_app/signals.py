from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from .models import CommentModel
from user_app.models import User
from django.dispatch import receiver
from group_app.models import GroupMember


# @receiver(post_save, sender=Comment)
# def user_comment_post(sender, instance, created, **kwargs):
#     if created:
#         print('notify_post_author')
#         comment_ins = instance
#         print('comment: ', comment_ins)
#         # course = comment.course
#         # print('course: ', course)
#         text_preview = comment_ins.comment[:90]
#         print('text_preview: ', text_preview)
#         sender = comment_ins.user
#         print('sender: ', sender)
#         receiver = comment_ins.course.author
#         print('receiver of comment: ', receiver)

#         # if sender != receiver: