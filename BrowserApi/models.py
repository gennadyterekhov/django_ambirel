from django.db import models


class ForumPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()
                             
    owner = models.ForeignKey('auth.User', related_name='forumPosts')

    class Meta:
        ordering = ('created',)

# 
# class ForumPostAttachment(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
