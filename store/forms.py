from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg. example@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})