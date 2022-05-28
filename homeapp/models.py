from django.db import models

# Create your models here.
class Corporation(models.Model):
    corp_id = models.IntegerField(null=False, primary_key=True)
    name = models.TextField(null=False, unique=True)
    summary = models.TextField(null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    dept_id = models.IntegerField(null=False)
    name = models.TextField(null=False)
    corp_name = models.ForeignKey(Corporation, to_field='name', on_delete=models.CASCADE, related_name='corp', db_column='corp_name')

    def __str__(self):
        return self.name