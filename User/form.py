from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from algorithm.base import getCountryCode


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2']


class RegisterForm(forms.ModelForm, forms.Form):
    gender_choices = [
        (0, 'Male'),
        (1, 'Female'),
        (2, 'Other'),
    ]
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=gender_choices,
        initial=0
    )
    # re_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))
    # country_code_choices = getCountryCode()
    # country_code = forms.ChoiceField(choices=country_code_choices, widget=forms.Select())

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'phone',
                  'first_name',
                  'last_name',
                  'day_of_birth']

    # def clean_phone(self):
    #     country_code = str(self.cleaned_data['country_code']).replace(' ', '')
    #     phone = str(self.cleaned_data['phone']).replace(' ', '')
    #     phone += country_code
    #     if len(phone) > 15:
    #         raise forms.ValidationError('Phone number is too long!')
    #     try:
    #         User.objects.get(phone=phone)
    #     except User.DoesNotExist:
    #         return phone
    #     raise forms.ValidationError('Phone number is already exist!')

    # def clean_password(self):
    #     if 'password' in self.cleaned_data:
    #         password = self.cleaned_data['password']
    #         re_password = self.cleaned_data['re_password']
    #         if password == re_password and password:
    #             return re_password
    #     raise forms.ValidationError("Password is invalid!")

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

    def save(self, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        phone = self.cleaned_data['phone']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        day_of_birth = self.cleaned_data['day_of_birth']
        gender = self.cleaned_data['gender']
        user = User.objects.create_user(username, email, password, phone, first_name, last_name, day_of_birth, gender)
        user.save()
