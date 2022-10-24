from django.utils.timezone import now
from django.db import models


class Regalia(models.Model):
    full_name = models.CharField('ФИО', max_length=256, unique=False)
    first_name = models.CharField('Имя', max_length=256, unique=False, null=True)
    second_name = models.CharField('Фамилия', max_length=256, unique=False, null=True)
    third_name = models.CharField('Отчество', max_length=256, unique=False, blank=True, null=True)
    en_regalia = models.CharField('EN Регалия', max_length=256, unique=False, null=True, blank=True)
    rank = models.CharField('Должности, звания', max_length=512, blank=True, unique=False)
    city = models.CharField('Город', max_length=128, unique=False)
    regalia = models.CharField('Регалия', max_length=512, blank=True)
    comments = models.TextField('Комментарии', blank=True)
    operation = models.ForeignKey('Operation', on_delete=models.CASCADE, null=True, blank=True)
    # is_en = models.BooleanField(default=False, null=True)

    # class Meta:
    #     unique_together = [['full_name', 'rank', 'regalia']]

    def __str__(self):
        return str(self.id)


class Operation(models.Model):
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.id)


class File(models.Model):
    zip_file = models.FileField(upload_to='zip', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_zip_file_url(self):
        return f"127.0.0.1:8000/media/{self.zip_file}"
