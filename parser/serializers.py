from rest_framework import serializers
from .models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
        ordering_fields = ['gender', 'age', 'city', 'work_experience', 'salary', 'updated_at']