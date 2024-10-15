from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Activity, Notification
from .serializers import UserSerializer, ActivitySerializer, NotificationSerializer, ActivityMetricsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import action

User = get_user_model()

class HomeView(APIView):
     permission_classes = [permissions.AllowAny]  # Allow access to everyone

     def get(self, request):
        return Response({"message": "Welcome to the Fitness Tracker API!"})

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, editing, and registering users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Serializer for retrieving user data
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Custom action for user registration.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing activity instances.
    """
    queryset = Activity.objects.all()  # Queryset for Activity model
    serializer_class = ActivitySerializer  # Serializer for Activity model
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['activity_type']  # Allows filtering by activity type
    ordering_fields = ['date']  # Optional ordering by date

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user) #filters user activities

        """Date Range Filter 
        (if both start date and end date parameters are present in the query request, activites are filtered with the range)"""
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        """Saves the activity with the logged-in user"""
        serializer.save(user=self.request.user)

        
class ActivityMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated
    serializer_class = ActivityMetricsSerializer  # Serializer for Activity model

    def get(self, request,):
        user = request.user
        period = request.query_params.get('period', 'weekly')  # Default to weekly if not specified

        if period == 'weekly':
            start_date = timezone.now() - timedelta(weeks=1)
        elif period == 'monthly':
            start_date = timezone.now() - timedelta(days=30)
        else:
            return Response ({"error": "Invalid period specified. Use 'weekly' or 'monthly'."}, status=400)
        
        # Filter activities for the user and the specified date range
        activities = Activity.objects.filter(user=user,date__gte = start_date)

        metrics = activities.aggregate (
            total_duration=Sum('duration', default=0),  # Total duration of all activities
            total_distance=Sum('distance', default=0),  # Total distance covered in activities
            total_calories=Sum('calories_burned', default=0)  # Total calories burned in activities
        )
       
        metrics_data = {
              'period': period,
              'total_duration': timedelta(minutes=metrics['total_duration']),
              'total_distance': metrics ['total_distance'],
              'total_calories': metrics ['total_calories']
        }
        
        serializer = ActivityMetricsSerializer(metrics_data)
        
        return Response(serializer.data)

    
class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notification instances.
    """
    queryset = Notification.objects.all()  # Queryset for Notification model
    serializer_class = NotificationSerializer  # Serializer for Notification model
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)