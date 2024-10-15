from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser. Adds a unique email field
    to ensure that each user has a unique email address.
    """
    email = models.EmailField(unique=True)  
    
    def __str__(self):
        return self.username

class Activity(models.Model):
    """ Represents a fitness activity performed by a user. Each activity is associated with
    a user and has attributes such as activity type, duration, distance, calories burned,
    and the date the activity was performed.
    """
    
    ACTIVITY_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Walking', 'Walking'),
        ('Weightlifting', 'Weightlifting' )
     ]
     
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'activities') #links Activity to the user
    activity_type = models.CharField(max_length=100, choices = ACTIVITY_CHOICES)
    duration = models.IntegerField() #minutes
    distance = models.FloatField() #km or miles
    calories_burned = models.PositiveIntegerField() #ensures the value cannot be negative
    date = models.DateTimeField(auto_now_add=True) #Stores date of activity

    def __str__(self):
        return f"{self.activity_type} by {self.user.username} on {self.date}"
class Notification(models.Model):
    """
    Model representing a notification for a user.
    Includes fields for the message, date, read status, and notification type.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') #Links Notification to user
    message = models.TextField() #Notification message
    date = models.DateTimeField(auto_now_add=True) #Records the notification was created automatically
    is_read = models.BooleanField(default=False) #Indicates if the notification have been read
    notification_type = models.CharField(max_length=20, default='general')

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]} on {self.date.strftime('%Y-%m-%d')}" #Displays first 50 characters of the message