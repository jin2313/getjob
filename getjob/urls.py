"""getjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from homeapp import views as homeviews
from homeapp.views import CorpView

urlpatterns = [
    # path('thres/', interviewviews.ThresView, name='thres'),
    path('admin/', admin.site.urls),
    path('', homeviews.MainView, name='home'),
    path('corps/', CorpView.as_view(), name='corp'),
    path('depts/', homeviews.DeptView, name='dept'),
    path('accounts/', include('accountapp.urls')),
    path('interviews/', include('interviewapp.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)