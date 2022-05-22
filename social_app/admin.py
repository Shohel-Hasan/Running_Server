from django.contrib import admin
from social_app.models import (
    CommentModel,
    FollowingModel
)
# Register your models here.
admin.site.register(CommentModel)
admin.site.register(FollowingModel)