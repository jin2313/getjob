from django.contrib import admin

from interviewapp.models import Question, Result

# Register your models here.
admin.site.register(Question)
admin.site.register(Result)