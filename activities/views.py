from django.db.models import Sum
from django.db.models.functions import TruncWeek
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User, Activity, WorkoutPlan, Goal, Notification
from .serializers import UserSerializer, ActivitySerializer, WorkoutPlanSerializer, GoalSerializer, NotificationSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_simplejwt.views import TokenObtainPairView

class HomeView(APIView):
     permission_classes = [permissions.AllowAny]  # Allow access to everyone

     def get(self, request):
        return Response({"message": "Welcome to the Fitness Tracker API!"})

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()  # Queryset for User model
    serializer_class = UserSerializer  # Serializer for User model
    permission_classes = [permissions.AllowAny]


class ActivityViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing activity instances.
    """
    queryset = Activity.objects.all()  # Queryset for Activity model
    serializer_class = ActivitySerializer  # Serializer for Activity model
    permission_classes = [IsAuthenticated]  # Requires authentication
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['activity_type']  # Allows filtering by activity type
    ordering_fields = ['date']  # Optional ordering by date

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user) #filters user activities

        # Date Range Filter (if both start date and end date parameters are present in the query request, activites are filtered with the range)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        # Save the activity with the current user
        serializer.save(user=self.request.user)

        
class ActivityMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Get the user's activity metrics by aggregating data
        user = request.user
        activities = Activity.objects.filter(user=user)

        weekly_trends = activities.annotate(week=TruncWeek('date')).values('week').annotate(
            total_duration=Sum('duration'),  # Total duration of all activities
            total_distance=Sum('distance'),  # Total distance covered in activities
            total_calories=Sum('calories_burned')  # Total calories burned in activities
        )

        return Response(weekly_trends)

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing workout plan instances.
    """
    queryset = WorkoutPlan.objects.all()  # Queryset for WorkoutPlan model
    serializer_class = WorkoutPlanSerializer  # Serializer for WorkoutPlan model
    permission_classes = [IsAuthenticated]  # Requires authentication


    def perform_create(self, serializer):
         # Save the activity with the current user
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing goal instances.
    """
    queryset = Goal.objects.all()  # Queryset for Goal model
    serializer_class = GoalSerializer  # Serializer for Goal model
    permission_classes = [IsAuthenticated]  # Requires authentication
    

    def perform_create(self, serializer):
        # Save the activity with the current user
        serializer.save(user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notification instances.
    """
    queryset = Notification.objects.all()  # Queryset for Notification model
    serializer_class = NotificationSerializer  # Serializer for Notification model
    permission_classes = [IsAuthenticated]  # Requires authentication

    def perform_create(self, serializer):
         # Save the activity with the current user
        serializer.save(user=self.request.user)

class CustomTokenObtainPairView(TokenObtainPairView):
    pass