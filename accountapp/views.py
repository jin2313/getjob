from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from . import forms


# Create your views here.
class SignupView(FormView):
    template_name = 'accountapp/signup.html'
    form_class = forms.SignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        id = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=id, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class SigninView(FormView):
    template_name = 'accountapp/signin.html'
    form_class = forms.SigninForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse('로그인 실패')
        return super().form_valid(form)