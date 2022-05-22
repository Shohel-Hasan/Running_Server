from django.db import models
from django.conf import settings
from group_app.models import Group
from core_app.models import BaseModel


# Create your models here.
class ThoughtPost(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='user_thought')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, related_name='group_thought')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-id']


class SummeryPost(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='user_summery')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, related_name='group_summery')
    title_of_research_article = models.CharField(max_length=150)
    objective_of_the_study = models.TextField(blank=True)
    theoritical_Background = models.TextField(blank=True)
    research_gap = models.TextField(blank=True)
    uniqueness_of_the_study = models.TextField(blank=True)
    data_source_sample_information = models.TextField(blank=True)
    research_methodology = models.TextField(blank=True)
    result_discussion = models.TextField(blank=True)
    validity_reliability_of_finding = models.TextField(blank=True)
    usefulness_of_the_finding = models.TextField(blank=True)
    reference = models.TextField(blank=True)
    annex = models.TextField(blank=True)
    file1 = models.FileField(upload_to='thought_post/', blank=True, null=True, )
    file2 = models.FileField(upload_to='thought_post/', blank=True, null=True, )
    keyword = models.TextField(blank=True)

    def __str__(self):
        return self.title_of_research_article

    class Meta:
        ordering = ['-id']


class CommentModel(models.Model):
    thought_post = models.ForeignKey(ThoughtPost, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='thought_post_comments')
    summary_post = models.ForeignKey(SummeryPost, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='summary_post_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comment_user')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.user.username}'

    def children(self):
        return CommentModel.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
