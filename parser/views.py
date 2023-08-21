from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from parser.hh_helpers import parser, parse_vacancies
from parser.models import Questionnaire
from parser.serializers import QuestionnaireSerializer


class QuestionnaireModelViewset(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class SearAPIView(APIView):
    def post(self, request):
        vacancy = request.data.get('vacancy')
        for counter in range(10):
            url = f'https://spb.hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&text=системный+администратор&enable_snippets=false&only_with_salary=true&L_save_area=true&page={counter}'
            # parser(2, vacancy, url)
            parse_vacancies(url)
        return Response({"message": "Закончил парсинг"}, status=status.HTTP_200_OK)


