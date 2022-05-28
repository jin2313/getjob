from django.urls import path

from interviewapp import views

app_name = 'interviewapp'

urlpatterns = [
    path('', views.QuestionView, name='question'),
    path('result/', views.ResultView, name='result'),
    path('report/', views.ReportView, name='report'),
]