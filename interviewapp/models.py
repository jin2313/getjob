from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Question(models.Model):
    quest_id = models.IntegerField(null=False, unique=True, default=0)
    level = models.IntegerField(null=False)
    content = models.TextField(null=False)

    def __str__(self):
        return str(self.quest_id)


class Result(models.Model):
    user_id = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, related_name='user', db_column='user_id')
    report_num = models.IntegerField(null=False, unique=False)
    quest_id = models.ForeignKey(Question, to_field='quest_id', on_delete=models.CASCADE, related_name='question', db_column='quest_id')
    result_stt = models.TextField(null=True)
    result_eye = models.TextField(null=True)
    result_face = models.TextField(null=True)
    result_add = models.TextField(null=True)

    def __str__(self):
        return f'{self.user_id}_{self.report_num}_{self.quest_id}'