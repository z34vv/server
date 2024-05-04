import datetime

from django.shortcuts import render, redirect
from .models import *
from .form import RegisterForm
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import (UserSerializer,
                          DemoUserSerializer)


class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user
        if user.is_manager or user.is_superuser:
            users = User.objects.filter(is_active=True)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        pass


class RegisterUserAPI(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_user(self, user_id):
        try:
            this_user = User.objects.get(user_id=user_id)
            if not this_user.is_active:
                return None
            else:
                return this_user
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        this_user = self.get_user(user_id)
        if this_user is None:
            return Response({'error': "This user does not exist!"})
        else:
            user = request.user
            view_mode = this_user.view_timeline_permission
            pms = False
            if user.is_manager or user.is_superuser or (user == this_user) or (view_mode == 0):
                pms = True
            else:
                if view_mode in [3, 1] and (user.user_id in this_user.friends):
                    pms = True
                elif view_mode <= 2 and (user.user_id in this_user.fans):
                    pms = True
                elif view_mode == 1 and (user.user_id in this_user.followers):
                    pms = True

            if pms:
                serializer = UserSerializer(this_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = DemoUserSerializer(this_user)
                return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        if user == this_user:
            serializer = UserSerializer(this_user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                this_user.updated_at = datetime.datetime.now()
                this_user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        if user == this_user:
            serializer = UserSerializer(this_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                this_user.updated_at = datetime.datetime.now()
                this_user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        if user.is_manager or user.is_superuser:
            this_user.is_active = False
            this_user.deleted_at = datetime.datetime.now()
            this_user.save()
            return Response({'message': "This user is deleted!"})
        return Response({'message': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)


class FollowAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, user_id):
        try:
            this_user = User.objects.get(user_id=user_id)
            if this_user.is_active:
                return this_user
        except User.DoesNotExist:
            return Response({'error': "This User does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        if user.user_id in this_user.followers:
            return Response({'status': 'Followed'})
        else:
            return Response({'status': 'UnFollow'})

    def patch(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        temp = '@' + user.user_id
        if temp in this_user.followers:
            follower_list = this_user.followers.split(temp)[1:]
            this_user.followers = ''.join(follower_list)
            this_user.save()
            follow_list = user.follows.split(('@' + this_user.user_id))[1:]
            user.follows = ''.join(follow_list)
            user.save()
            return Response({'status': 'UnFollowed!'}, status=status.HTTP_200_OK)
        else:
            this_user.followers += temp
            this_user.save()
            user.follows += ('@' + this_user.user_id)
            user.save()
            return Response({'status': 'Followed!'}, status=status.HTTP_200_OK)


class BecomeFanAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, user_id):
        try:
            this_user = User.objects.get(user_id=user_id)
            if this_user.is_active:
                return this_user
        except User.DoesNotExist:
            return Response({'error': "This User does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        if user.user_id in this_user.fans:
            return Response({'status': 'True'})
        else:
            return Response({'status': 'False'})

    def patch(self, request, user_id):
        this_user = self.get_user(user_id)
        user = request.user
        temp = '@' + user.user_id
        if temp in this_user.fans:
            fan_list = this_user.fans.split(temp)[1:]
            this_user.fans = ''.join(fan_list)
            this_user.save()
            idol_list = user.idols.split(('@' + this_user.user_id))[1:]
            user.idols = ''.join(idol_list)
            user.save()
            return Response({'status': 'Canceled!'}, status=status.HTTP_200_OK)
        else:
            user_bag = Bag.objects.get(user=user)
            if user_bag.sapphires >= 25:
                user_bag.sapphires -= 25
                this_user_bag = Bag.objects.get(user=this_user)
                this_user_bag.sapphires += 20
                this_user_bag.save()
                user_bag.save()
                this_user.fans += temp
                this_user.save()
                user.idols += ('@' + this_user.user_id)
                user.save()
                return Response({'status': 'Became a fan!'}, status=status.HTTP_200_OK)
            else:
                return Response({'mesage': "You must have at least 25 sapphires in your bag!"}, status=status.HTTP_400_BAD_REQUEST)


class GiftAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, receiver_id, gift_code):
        gift = {1: ('flower', 10),
                2: ('phone', 50),
                3: ('car', 100),
                4: ('plane', 200),
                5: ('rocket', 500)}
        user = request.user
        receiver = User.objects.get(user_id=receiver_id)
        user_bag = Bag.objects.get(user=user)
        receiver_bag = Bag.objects.get(user=receiver)
        price = gift[gift_code][1]
        if user_bag.sapphires >= price:
            user_bag.sapphires -= price
            user_bag.save()
            receiver_bag.sapphires += int(price*0.8)
            receiver_bag.save()
            return Response({'message': f"You donated the {gift[gift_code][0]}!"}, status=status.HTTP_200_OK)
        return Response({'error': "Your account is insufficient!"}, status=status.HTTP_400_BAD_REQUEST)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
