from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView, UserViewSet, ActivityViewSet, NotificationViewSet, ActivityMetricsView, ApiRootViewAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'activities', ActivityViewSet)
router.register(r'notifications', NotificationViewSet)


urlpatterns = [
    path('auth/', ApiRootViewAuthenticated.as_view(), name='api_root_authenticated'),  # Authenticated API root
    path('home/', HomeView.as_view(), name='home'),
    path('activity-metrics/', ActivityMetricsView.as_view(), name='activity-metrics'), 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
