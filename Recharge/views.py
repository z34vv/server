from django.shortcuts import render


def generateSapphireCode(request):
    user = request.user
    if user.is_manager or user.is_superuser:
        if request.method == 'POST':
            pass
