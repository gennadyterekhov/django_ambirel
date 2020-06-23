from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from browserapi.models import ForumPost


class ForumPostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail')

    class Meta:
        model = ForumPost
        fields = ('created', 'title', 'content', 'owner')
        
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    forumPosts = serializers.HyperlinkedRelatedField(many=True, view_name='forumPost-detail')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'forumPosts')
