from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Activity, WorkoutPlan, Goal, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' #Includes all the field from the model
        extra_kwargs = {'password': {'write_only': True}} #Makes password field writeonly (won't be included in the serializer output when reading)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password to ensure security
        user.save() # Save the new User object to the database, now with the hashed password.
        return user
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)  # Hash the new password if provided
        instance.save()
        return instance

class ActivitySerializer(serializers.ModelSerializer):
     user = serializers.StringRelatedField(read_only=True)  # Shows the username instead of user ID
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
     
class WorkoutPlanSerializer(serializers.ModelSerializer):
     user = serializers.StringRelatedField(read_only=True)  # Displays username for the user
     activities = ActivitySerializer(many=True, read_only=True)  # Nested serializer for activities
     class Meta:
        model = WorkoutPlan
        fields = '__all__' #Includes all the field from the model
        read_only_fields = ['user_id', 'date'] # User ID and date are set automatically

class GoalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows the username instead of user ID
    class Meta:
        model = Goal
        fields = '__all__' #Includes all the field from the model
        read_only_fields = ['user_id', 'date'] # User ID and date are set automatically
class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows the username instead of user ID
    class Meta:
        model = Notification
        fields = '__all__' #Includes all the field from the model
        read_only_fields = ['user_id', 'date'] # User ID and date are set automatically