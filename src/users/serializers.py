from rest_framework import serializers

class UserCreationSerializer(serializers.Serializer):    
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    created_at = serializers.DateTimeField()
    
class UserProfileSerializer(serializers.Serializer): 
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    created_at = serializers.DateTimeField()
    followers = serializers.IntegerField()
    following = serializers.IntegerField()