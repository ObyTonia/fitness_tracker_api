from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Activity, Notification

User = get_user_model()

class FitnessTrackerApiTests(APITestCase):

    def setUp(self):
        """Create a user and sample data for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.activity_url = reverse('activity-list')
        self.notification_url = reverse('notification-list')
        self.metrics_url = reverse('activity-metrics')  # You might need to define this URL in your urlpatterns

        response = self.client.post(reverse('token_obtain_pair'), {
        'username': 'testuser',
        'password': 'testpassword'
    })
        self.token = response.data['access']  # Adjust based on your token setup
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  # Set the token for requests

    def test_home_view(self):
        """Test the home view."""
        response = self.client.get(reverse('home'))  # Ensure you have named your home view in urls
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Welcome to the Fitness Tracker API!"})

    def test_user_registration(self):
        """Test user registration."""
        url = reverse('user-register')  # Adjust according to your URL patterns
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'newuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Check if user count increased

    def test_activity_creation(self):
        """Test activity creation."""
        data = {
            'activity_type': 'Running',
            'duration': 30,
            'distance': 5,
            'calories_burned': 300,
            'date': '2024-10-01',
        }
        response = self.client.post(self.activity_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)  # Check if activity count is 1

    def test_get_activity_metrics(self):
        """Test retrieving activity metrics."""
        # First, create an activity to calculate metrics
        Activity.objects.create(
            user=self.user,
            activity_type='Running',
            duration=30,
            distance=5,
            calories_burned=300,
            date='2024-10-01',
        )
        response = self.client.get(self.metrics_url, {'period': 'weekly'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_duration'], '00:30:00')

    def test_notification_creation(self):
        """Test notification creation."""
        data = {
            'message': 'Test notification',
            'date': '2024-10-01',
        }
        response = self.client.post(self.notification_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)  # Check if notification count is 1

    def test_unauthenticated_user_access(self):
        """Test that unauthenticated users cannot access activity endpoint."""
        self.client.logout()
        response = self.client.get(self.activity_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Ensure access is denied

