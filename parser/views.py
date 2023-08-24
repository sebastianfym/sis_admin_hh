from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from parser.hh_helpers import parse_vacancies, parse_sys_admin_who_work_in_real_time
from parser.models import Questionnaire
from parser.serializers import QuestionnaireSerializer
from user.models import User


class QuestionnaireModelViewset(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class SearAPIView(APIView):
    def post(self, request):
        vacancy = request.data.get('vacancy')
        for counter in range(10):
            url = f'https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=системный+администратор&enable_snippets=false&only_with_salary=true&L_save_area=true&page={counter}'
            # parser(2, vacancy, url)
            auth_cookies = [
                {'name': 'auth_token', 'value': 'yw3eCClDS8Q4zDVmfc2ZT6L5jkF3'}
            ]
            parse_vacancies(url, auth_cookies)

        return Response({"message": "Закончил парсинг"}, status=status.HTTP_200_OK)


# hhtoken	yw3eCClDS8Q4zDVmfc2ZT6L5jkF3	.hh.ru	/	2024-09-27T11:08:07.706Z	35	✓	✓	None		Medium

class SearchSysAdminWorkInRTAPI(APIView):

    def post(self, request):
        boss = User.objects.filter(access_token__isnull=False).first()
        vacancy, area_id, access_token = 'системный администратор', 2, boss.access_token
        parse_sys_admin_who_work_in_real_time(vacancy, area_id, access_token)
        questionnaire = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaire, many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)
