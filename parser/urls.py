from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import QuestionnaireModelViewset, SearAPIView

router = DefaultRouter()

# router.register('questionnaire', QuestionnaireModelViewset)
# router.register('get_perm', GetPermissionForAPI)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', SearAPIView.as_view()),

]