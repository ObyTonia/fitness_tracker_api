from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Email field with unique constraint
    
    def __str__(self):
        return self.username

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Walking', 'Walking'),
        ('Weightlifting', 'Weightlifting' )
     ]
     
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'activities') #links to the user
    activity_type = models.CharField(max_length=100, choices = ACTIVITY_CHOICES)
    duration = models.IntegerField() #minutes
    distance = models.FloatField() #km or miles
    calories_burned = models.PositiveIntegerField() #ensures the value cannot be negative
    date = models.DateTimeField(auto_now_add=True) #Stores date of activity

    def __str__(self):
        return f"{self.activity_type} by {self.user_id.username} on {self.date}"
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') #Links Notification to user
    message = models.TextField() #Notification message
    date = models.DateTimeField(auto_now_add=True) #Records the notification was created automatically
    is_read = models.BooleanField(default=False) #Indicates if the notification have been read
    notification_type = models.CharField(max_length=20, default='general')

    def __str__(self):
        return f"Notification for {self.user_id.username}: {self.message[:50]} on {self.date.strftime('%Y-%m-%d')}" #Displays first 50 characters of the message