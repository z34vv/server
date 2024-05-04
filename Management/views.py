from django.shortcuts import render, redirect
from User.models import *
from User.form import RegisterForm
from Post.models import *
from Chat.models import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
# Create your views here.


class ManagementView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        user = request.user
        if user.is_manager or user.is_admin:
            return render(request, 'management/index.html')


def createUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(request.META.get('HTTP_REFERER'))


def listUser(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'management/index.html', {'users': users})
