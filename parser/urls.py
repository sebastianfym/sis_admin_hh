from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import QuestionnaireModelViewset, SearchSysAdminVacanciesAPIView, RefreshAccessDataApiView, \
    SearchSysAdminWorkInRTAPI, SysAdminInCompany

router = DefaultRouter()

# router.register('questionnaire', QuestionnaireModelViewset)
# router.register('get_perm', GetPermissionForAPI)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', SearchSysAdminVacanciesAPIView.as_view()),
    path('access_code/', RefreshAccessDataApiView.as_view(), name='access_view'),
    path('search_api/', SearchSysAdminWorkInRTAPI.as_view(), name='search_api'),
    path('sys_admin_search_company/', SysAdminInCompany.as_view(), name='sys_admin_search_company')

]