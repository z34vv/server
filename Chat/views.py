from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from User.models import User, Bag
from .serializers import MessageSerializer, CreateMessageSerializer, MsgUserSerializer
from django.db.models import Subquery, OuterRef, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


class MyInbox(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user

        messages = Message.objects.filter(
            message_id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user.user_id) |
                    Q(receiver__sender=user.user_id)
                ).distinct().annotate(last_msg=Subquery(
                    Message.objects.filter(
                        Q(sender=OuterRef('user_id'), receiver=user.user_id) |
                        Q(receiver=OuterRef('user_id'), sender=user.user_id)
                    ).order_by('-message_id')[:1].values_list('message_id', flat=True)
                )).values_list('last_msg', flat=True).order_by('-user_id')
            )
        ).order_by('-message_id')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessagesAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request, receiver_id):
        sender = request.user
        receiver = User.objects.get(user_id=receiver_id)

        messages = Message.objects.filter(sender__in=[sender, receiver], receiver__in=[sender, receiver]).order_by(
            '-created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, receiver_id):
        sender = request.user
        receiver = User.objects.get(user_id=receiver_id)
        serializer = CreateMessageSerializer(data=request.data, sender=sender, receiver=receiver)

        if serializer.is_valid():
            msg_instance = serializer.save()
            if 'images' in request.data:
                images_data = request.FILES.getlist('images')

                for image_data in images_data:
                    image = MessageImage.objects.create(message=msg_instance, image=image_data)
                    msg_instance.images.add(image)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request, username):
        users = User.objects.filter(username__icontains=username)
        if not users.exists():
            return Response({'message': "No user founds"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MsgUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        user = request.user

        last_msgs = Message.objects.filter(
            message_id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user.user_id) |
                    Q(receiver__sender=user.user_id)
                ).distinct().annotate(last_msg=Subquery(
                    Message.objects.filter(
                        Q(sender=OuterRef('user_id'), receiver=user.user_id) |
                        Q(receiver=OuterRef('user_id'), sender=user.user_id)
                    ).order_by('-message_id')[:1].values_list('message_id', flat=True)
                )).values_list('last_msg', flat=True).order_by('-user_id')
            )
        ).order_by('-created_at')
        if len(last_msgs) != 0:
            if last_msgs[0].sender == user:
                index = last_msgs[0].receiver.username
            else:
                index = last_msgs[0].sender.username
        # return redirect('chat-box/{index}/')
        return render(request, 'chat/chatIndex.html', {'last_msgs': last_msgs})


class ChatBox(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request, *args, **kwargs):
        user = request.user

        partner = get_object_or_404(User, username=self.kwargs['username'])

        last_msgs = Message.objects.filter(
            message_id__in=Subquery(
                User.objects.filter(
                    Q(sender__receiver=user.user_id) |
                    Q(receiver__sender=user.user_id)
                ).distinct().annotate(last_msg=Subquery(
                    Message.objects.filter(
                        Q(sender=OuterRef('user_id'), receiver=user.user_id) |
                        Q(receiver=OuterRef('user_id'), sender=user.user_id)
                    ).order_by('-message_id')[:1].values_list('message_id', flat=True)
                )).values_list('last_msg', flat=True).order_by('-user_id')
            )
        ).order_by('-created_at')

        msgs = Message.objects.filter(sender__in=[user, partner], receiver__in=[user, partner]).order_by(
            'created_at')[:50]
        all_msg = Message.objects.filter(sender=partner, receiver=user, is_read=False)
        for msg in all_msg:
            msg.is_read = True
            msg.save()

        context = {'partner': partner,
                   'last_msgs': last_msgs,
                   'msgs': msgs}
        return render(request, 'chat/chat.html', context)


def sendMessage(request, partner_name):
    if request.htmx:
        sender = request.user
        receiver = User.objects.get(username=partner_name)
        content = request.POST.get('content')
        if content:
            msg = Message.objects.create(sender=sender, receiver=receiver, content=content)
            return render(request, 'chat/chat_msg_p.html', {'msg': msg})
    # if request.method == 'POST':
    #     sender = request.user
    #     receiver = User.objects.get(username=partner_name)
    #     content = request.POST.get('content')
    #     this_msg = Message(sender=sender, receiver=receiver, content=content)
    #     this_msg.save()
    # return redirect(request.META.get('HTTP_REFERER'))


def donateGift(request, receiver_name, gift_code):
    sender = request.user
    sender_bag = Bag.objects.get(user=sender)
    receiver = User.objects.get(username=receiver_name)
    receiver_bag = Bag.objects.get(user=receiver)
    gift = {1: ('flower', 10),
            2: ('phone', 50),
            3: ('car', 100),
            4: ('plane', 200),
            5: ('rocket', 500)}
    price = gift[gift_code][1]
    if sender_bag.sapphires >= price:
        sender_bag.sapphires -= price
        sender_bag.save()
        receiver_bag.sapphires += int(price * 0.8)
        receiver_bag.save()
        msg = f"{sender.username} donate {gift[gift_code][0]} (+{price} sapphires)!"
        Message.objects.create(sender=sender, receiver=receiver, content=msg)
    return redirect(request.META.get('HTTP_REFERER'))


def searchUser(request):
    query = request.GET.get('query')
    if query:
        result = get_object_or_404(User, username__icontains=query)

        last_msg = {}
        for u in result:
            msg = Message.objects.filter(sender__in=[u, request.user], receiver__in=[u, request.user]).order_by('-created_at')[0]
            last_msg[str(u.username)] = msg.content

        return render(request, 'chat/chatSearch.html', {'result': result, 'last_msg': last_msg})
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))
