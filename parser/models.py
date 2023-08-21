from django.db import models


class Questionnaire(models.Model):
    link = models.URLField(max_length=5000, blank=True, null=True, verbose_name='Ссылка на hh.ru')
    vacancy = models.CharField(max_length=500, blank=True, null=True, verbose_name='Вакансия')
    gender = models.CharField(max_length=500, blank=True, null=True, verbose_name='Гендер')
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город проживания')
    company_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='Название компании')
    work_in_real_time = models.CharField(max_length=600, blank=True, null=True)
    work_experience = models.CharField(max_length=500, blank=True, null=True, verbose_name='Общий опыт работы')
    birthday = models.CharField(max_length=100, blank=True, null=True, verbose_name='День рождения')
    salary = models.PositiveIntegerField(blank=True, null=True, verbose_name='Зарплата')
    education = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Образование')
    photo_link = models.URLField(max_length=5000, blank=True, null=True, verbose_name='Ссылка на фото')
    updated_at = models.CharField(max_length=100, blank=True, null=True, verbose_name='Последнее обновление')

    def __str__(self):
        return f'{self.id}, {self.vacancy}, {self.gender}, {self.age}, {self.city}, {self.company_name}, {self.work_in_real_time},' \
               f'{self.work_experience}, {self.salary}, {self.education}, {self.link}, {self.photo_link}, {self.updated_at}'

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'
