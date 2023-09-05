from django.db import models


class Questionnaire(models.Model):

    vacancy = models.CharField(max_length=500, blank=True, null=True, verbose_name='Вакансия')
    company = models.CharField(max_length=500, blank=True, null=True, verbose_name='Компания')
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='Адрес')
    experience = models.CharField(max_length=300, blank=True, null=True, verbose_name='Опыт работы')
    contacts = models.CharField(max_length=600, blank=True, null=True, verbose_name='контакты')
    read = models.BooleanField(default=False, verbose_name='Использовалась')

    def __str__(self):
        return f'{self.id}, {self.vacancy}, {self.address}, {self.experience}, {self.contacts}'

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'
