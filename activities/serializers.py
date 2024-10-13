# from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Activity, Notification

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} #Makes password field writeonly (won't be included in the serializer output when reading)

    def create(self, validated_data):
        """Overriding create method to handle password hashing"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class ActivitySerializer(serializers.ModelSerializer):
     user = serializers.StringRelatedField(read_only=True)  
     class Meta:
        model = Activity
        fields = '__all__' #Includes all the field from the model
        read_only_fields = ['user_id', 'date'] # User ID and date are set automatically
        
     def validate_activity_type(self, value):
        if not value:
            raise serializers.ValidationError("Activity Type is required.")
        return value
     def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive value in minutes.")
        return value
     def validate_distance(self, value):
        if value < 0:
            raise serializers.ValidationError("Distance cannot be negative.")
        return value
    
class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows the username instead of user ID
    class Meta:
        model = Notification
        fields = '__all__' #Includes all the field from the model
        read_only_fields = ['date'] # User ID and date are set automatically

class ActivityMetricsSerializer (serializers.Serializer):
    period = serializers.ChoiceField(choices=['weekly', 'monthly'])
    total_distance = serializers.FloatField()
    total_calories = serializers.IntegerField()
    total_duration = serializers.DurationField()