from django.contrib import admin
from post_app.models import ThoughtPost, SummeryPost, CommentModel

# Register your models here.
admin.site.register(ThoughtPost)
admin.site.register(SummeryPost)
admin.site.register(CommentModel)
