from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    # email = models.EmailField(unique=True)  # Email field with unique constraint
    # password = models.CharField(max_length=128)  # Password field (hashed)
    # date = models.DateTimeField(auto_now_add=True)  # automatically indicates when the user was created

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
    duration = models.DurationField() #minutes
    distance = models.FloatField() #km or miles
    calories_burned = models.PositiveIntegerField() #ensures the value cannot be negative
    date = models.DateTimeField(auto_now_add=True) #Stores date of activity

    def __str__(self):
        return f"{self.activity_type} by {self.user_id.username} on {self.date}"
    

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')  # Each plan belongs to a user
    name = models.CharField(max_length=100)  # Name of the workout plan
    activities = models.ManyToManyField(Activity, related_name='workout_plans')  # Activities associated with the plan
    date = models.DateTimeField(auto_now_add=True)  # automatically shows when the plan was created

    def __str__(self):
        return f"{self.name} by {self.user_id.username} (Created on: {self.date.strftime('%Y-%m-%d')})"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    target = models.FloatField() #target distance, calories, duration etc.
    current_progress = models.FloatField(default=0)  # Progress toward the goal
    start_date = models.DateField()  # Start date for tracking the goal
    deadline = models.DateTimeField() #deadline for tracking the goal
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"Goal for {self.user_id.username}: {self.target} - Achieved: {self.achieved}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications') #Links Notification to user
    message = models.TextField() #Notification message
    date = models.DateTimeField(auto_now_add=True) #Records the notification was created automatically
    is_read = models.BooleanField(default=False) #Indicates if the notification have been read
    notification_type = models.CharField(max_length=20, default='general',  choices=[('reminder', 'Reminder'),('goal_achieved', 'Goal Achieved'),])

    def __str__(self):
        return f"Notificatio for {self.user_id.username}: {self.message[:50]} on {self.date.strftime('%Y-%m-%d')}" #Displays first 50 characters of the message