from django.contrib import admin
from .models import User, Activity, Notification

# Customizing the User admin interface
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username',)
    ordering = ('username',)

# Customizing the Activity admin interface
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration', 'distance', 'calories_burned', 'date')
    search_fields = ('user__username', 'activity_type')
    list_filter = ('activity_type', 'date')
    ordering = ('-date',)  # Order by date descending

# Customizing the Notification admin interface
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'date', 'notification_type')
    search_fields = ('user__username', 'message', 'notification_type')
    list_filter = ('is_read', 'notification_type', 'date')
    ordering = ('-date',)  # Order by date descending
