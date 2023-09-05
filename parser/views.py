import openpyxl
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .helpers.token_helpers import *
from parser.helpers.hh_helpers import parse_sys_admin_who_work_in_real_time, parse_vacancies_sys_admin, parse_vacancies
from parser.models import Questionnaire
from parser.serializers import QuestionnaireSerializer
from user.models import User


class QuestionnaireModelViewset(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class SearchSysAdminVacanciesAPIView(APIView):
    def post(self, request):
        vacancy = request.data.get('vacancy')
        city = 2  # request.data.get('city') #Todo менять значение города на значение area_id из словаря
        boss = User.objects.filter(access_token__isnull=False).first()

        # url = f'https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=системный+администратор&enable_snippets=false&only_with_salary=true&L_save_area=true&page={page_number}'

        for page_number in range(20):
            parse_vacancies_sys_admin(vacancy, city, boss.access_token, page_number)
        return Response({"message": "Закончил парсинг"}, status=status.HTTP_200_OK)


# hhtoken	yw3eCClDS8Q4zDVmfc2ZT6L5jkF3	.hh.ru	/	2024-09-27T11:08:07.706Z	35	✓	✓	None		Medium
# 1692950015_9dda952e2d4ef36fe0371383c7702351fbfa7a289289fa02f760c2e3a1b07c61
"""
hhul=db3765a64829c9cfa1698ce18b5ee30869fc91e85785a06cef5de0627ba9534f; hhtoken=IdsKX5ixTyxamZKf1igeVrxGSshi; _hi=151696165;
"""


class SearchSysAdminWorkInRTAPI(APIView):

    def get(self, request):
        boss = User.objects.filter(access_token__isnull=False).first()
        vacancy, area_id, access_token = 'Системный администратор', 2, boss.access_token
        parse_sys_admin_who_work_in_real_time(vacancy, area_id, access_token)
        # questionnaire = Questionnaire.objects.all()
        # serializer = QuestionnaireSerializer(questionnaire, many=True)
        # return Response({"message": serializer.data}, status=status.HTTP_200_OK)
        response = FileResponse(open('result_admin.xlsx', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="your_filename.csv"'
        return response
        # return Response()


class SysAdminInCompany(APIView):
    def get(self, request):
        url = 'https://hh.ru'
        parse_vacancies()
        response = FileResponse(open('company_who_search_sys_admin.xlsx', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="your_filename.csv"'
        return response


class RefreshAccessDataApiView(APIView):
    def get(self, request, *args, **kwargs):
        authorization_code = request.query_params.get('code')
        access_code = get_access_token(authorization_code)

        return Response({'detail': f'{access_code}'})


class GetSheetAPI(APIView):
    def get(self, request):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Название вакансии', 'Компания', 'Адрес', 'Опыт', 'контакты'])
        questionnaires = Questionnaire.objects.filter(read=False)
        for questionnaire in questionnaires:
            sheet.append([questionnaire.vacancy, questionnaire.company, questionnaire.address,
                          questionnaire.experience, questionnaire.contacts])
            questionnaire.read = True
            questionnaire.save()

        file_path = "company_who_search_sys_admin.xlsx"
        workbook.save(file_path)
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="company_who_search_sys_admin.csv"'
        return response