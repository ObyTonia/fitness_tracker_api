from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView, UserViewSet, ActivityViewSet, WorkoutPlanViewSet, GoalViewSet, NotificationViewSet, ActivityMetricsView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'notifications', NotificationViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', HomeView.as_view(), name='home'),  # Home page route
    path('activity-metrics/', ActivityMetricsView.as_view(), name='activity-metrics'), 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='login'),
]
