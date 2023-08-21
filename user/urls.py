from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import Authentication, Profile, UserViewSet, LogoutView

router = DefaultRouter()

router.register('auth', Authentication)
router.register('profile', Profile)
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view())
]