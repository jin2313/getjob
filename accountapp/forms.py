from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignupForm(ModelForm):
    password = forms.CharField(max_length=20, label='', help_text='', widget=forms.PasswordInput(attrs={
        'class': 'account-form form-control w-100 mb-3',
        'placeholder': '비밀번호'
    }))
    confirm_password = forms.CharField(max_length=20, label='', help_text='', widget=forms.PasswordInput(attrs={
        'class': 'account-form form-control w-100 mb-3',
        'placeholder': '비밀번호 확인'
    }))
    class Meta:
        model = User
        fields = ['username', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'account-form form-control w-100 mb-3',
                'placeholder': '아이디'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'account-form form-control w-100 mb-3',
                'placeholder': '이름'
            })
        }
        labels = {'username': '', 'last_name': ''}
        help_texts = {'username': ''}

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password1

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        id = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user.username = id
        user.set_password(password)
        user.save()
        return user


class SigninForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'account-form form-control w-100 mb-3',
        'placeholder': '아이디'
    }))
    password = forms.CharField(max_length=20, label='', help_text='', widget=forms.PasswordInput(attrs={
        'class': 'account-form form-control w-100 mb-3',
        'placeholder': '비밀번호'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error('password', forms.ValidationError('비밀번호가 틀렸습니다.'))
        except User.DoesNotExist:
            self.add_error("username", forms.ValidationError('계정이 존재하지 않습니다.'))