from rest_framework import serializers

class PostCreationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    comments = serializers.JSONField()
    
class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    comments = serializers.JSONField()