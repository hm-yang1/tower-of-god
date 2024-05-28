from rest_framework import serializers
from ..models.user import User

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance:User, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'date_created', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}