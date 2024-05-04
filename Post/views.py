import datetime
import random

from .models import *
from User.models import User
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (PostCreateSerializer,
                          PostSerializer,
                          PostCommentCreateSerializer,
                          PostCommentSerializer,
                          RepPostCommentCreateSerializer,
                          RepPostCommentSerializer,
                          ImageSerializer,
                          HashtagSerializer)


class HomeView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request):
        data = {'Posts': Post.objects.filter(deleted_at__isnull=True)}
        return render(request, 'home.html', data)


class PostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user
        if user.is_manager or user.is_superuser:
            posts = Post.objects.filter(deleted_at__isnull=True)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Unauthorized to perform this operation!'}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        author = request.user
        post_serializer = PostCreateSerializer(data=request.data, author=author)

        if post_serializer.is_valid():
            post_instance = post_serializer.save()
            if 'images' in request.data:
                images_data = request.FILES.getlist('images')

                for image_data in images_data:
                    image = PostImage.objects.create(post=post_instance, image=image_data)
                    post_instance.images.add(image)
                return Response(post_serializer.data, status=status.HTTP_201_CREATED)

            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_post(self, pk):
        try:
            post = Post.objects.get(post_id=pk)
            if post.deleted_at:
                post = None
        except Post.DoesNotExist:
            post = None
        return post

    def get(self, request, pk):
        this_post = self.get_post(pk)
        if this_post is None:
            return Response({'error': "This Post does not exist!"})
        else:
            serializer = PostSerializer(this_post)
            user = request.user
            author = this_post.author
            if (this_post.author == user) or user.is_manager or user.is_superuser or (this_post.view_mode == 0):
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Only followers of post owner can view
                if (this_post.view_mode == 1) and user.user_id in author.followers:
                    return Response(serializer.data, status=status.HTTP_200_OK)

                # Only fans of post owner can view
                elif (this_post.view_mode == 2) and (user.user_id in author.fans):
                    return Response(serializer.data, status=status.HTTP_200_OK)

                # Only friends of post owner can view
                elif (this_post.view_mode == 3) and user.user_id in author.friends:
                    return Response(serializer.data, status=status.HTTP_200_OK)

                elif this_post.view_mode == 4:
                    return Response({'errors': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)

                return Response({'message': "The view mode does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        this_post = self.get_post(pk)
        user = request.user
        if user.user_id == this_post.author.user_id:
            serializer = PostSerializer(this_post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                this_post.updated_at = datetime.datetime.now()
                this_post.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        this_post = self.get_post(pk)
        user = request.user
        if this_post.author == user:
            serializer = PostSerializer(this_post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                this_post.updated_at = datetime.datetime.now()
                this_post.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        this_post = self.get_post(pk)
        user = request.user
        if (user.user_id == this_post.author.user_id) or user.is_manager or user.is_superuser:
            this_post.deleted_at = datetime.datetime.now()
            this_post.save()
            return Response({'message': 'Post deleted successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Unauthorized to perform this operation!'}, status=status.HTTP_403_FORBIDDEN)


class PostLike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        try:
            this_post = Post.objects.get(post_id=post_id)
            user = request.user
            if user.user_id in this_post.like_users:
                return Response({'status': 'Liked'})
            else:
                return Response({'status': "Don't like yet"})
        except Post.DoesNotExist:
            return Response({'error': "This post dose not exist!"})

    def patch(self, request, post_id):
        try:
            this_post = Post.objects.get(post_id=post_id)
            user = request.user
            temp = '@' + user.user_id
            if user.user_id in this_post.like_users:
                temp_list = this_post.like_users.split(temp)
                this_post.like_users = ''.join(temp_list)
                this_post.save()
                return Response({'status': 'Unliked'})
            else:
                this_post.like_users += ('@' + user.user_id)
                this_post.save()
                return Response({'status': 'Liked'})
        except Post.DoesNotExist:
            return Response({'error': "This post dose not exist!"})


class NewFeedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user

        idol_list = str(user.idols).split('@')[1:]
        idol_posts = []
        for author_id in idol_list:
            author = User.objects.get(user_id=author_id)
            posts = Post.objects.filter(author=author, view_mode__in=[0, 1, 4], deleted_at__isnull=True)
            for post in posts:
                idol_posts.append(post)

        friend_list = str(user.friends).split('@')[1:]
        for friend_id in friend_list:
            if friend_id in idol_list:
                friend_list.remove(friend_id)
        friend_posts = []
        for author_id in friend_list:
            author = User.objects.get(user_id=author_id)
            posts = Post.objects.filter(author=author, view_mode__in=[0, 5], deleted_at__isnull=True)
            for post in posts:
                friend_posts.append(post)

        follow_list = str(user.follows).split('@')[1:]
        for author_id in follow_list:
            if (author_id in idol_list) or (author_id in friend_list):
                follow_list.remove(author_id)
        follow_posts = []
        for author_id in follow_list:
            author = User.objects.get(user_id=author_id)
            posts = Post.objects.filter(author=author, view_mode__lt=1, deleted_at__isnull=True)
            for post in posts:
                follow_posts.append(post)

        new_feed_post = idol_posts + friend_posts + follow_posts
        random.shuffle(new_feed_post)

        serializer = PostSerializer(new_feed_post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCommentApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        user = request.user
        this_post = Post.objects.get(post_id=post_id)
        comments = Comment.objects.filter(post=this_post)
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id, *args, **kwargs):
        this_post = Post.objects.get(post_id=post_id)
        user = request.user
        pms = False
        if user.is_manager or user.is_superuser or (user == this_post.author) or (this_post.chat_mode == 0):
            pms = True
        elif (this_post.chat_mode in [3, 1]) and (user.user_id in this_post.author.friends):
            pms = True
        elif (this_post.chat_mode <= 2) and (user.user_id in this_post.author.fans):
            pms = True
        elif (this_post.chat_mode == 1) and (user.user_id in this_post.author.friends):
            pms = True

        if pms:
            comment_serializer = PostCommentCreateSerializer(data=request.data, author=user, post=this_post)
            if comment_serializer.is_valid():
                comment_serializer.save()
                this_post.comment_count += 1
                this_post.save()
                return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)


class CommentLike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cmt_id):
        try:
            this_cmt = Comment.objects.get(comment_id=cmt_id)
            user = request.user
            if user.user_id in this_cmt.like_users:
                return Response({'status': 'Liked'})
            else:
                return Response({'status': "Don't like yet"})
        except Comment.DoesNotExist:
            return Response({'error': "This post dose not exist!"})

    def patch(self, request, cmt_id):
        try:
            this_cmt = Comment.objects.get(comment_id=cmt_id)
            user = request.user
            temp = '@' + user.user_id
            if temp in this_cmt.like_users:
                temp_list = this_cmt.like_users.split(temp)
                this_cmt.like_users = ''.join(temp_list)
                this_cmt.save()
                return Response({'status': 'Unliked'})
            else:
                this_cmt.like_users += ('@' + user.user_id)
                this_cmt.save()
                return Response({'status': 'Liked'})
        except Comment.DoesNotExist:
            return Response({'error': "This post dose not exist!"})


class RepPostCommentApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id, cmt_id):
        main_cmt = Comment.objects.get(comment_id=cmt_id)
        rep_comments = RepComment.objects.filter(main_cmt=main_cmt)
        serializer = RepPostCommentSerializer(rep_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id, cmt_id, *args, **kwargs):
        this_post = Post.objects.get(post_id=post_id)
        main_cmt = Comment.objects.get(comment_id=cmt_id)
        user = request.user
        pms = False
        if user.is_manager or user.is_superuser or (user == this_post.author) or (this_post.chat_mode == 0):
            pms = True
        elif (this_post.chat_mode in [3, 1]) and (user.user_id in this_post.author.friends):
            pms = True
        elif (this_post.chat_mode <= 2) and (user.user_id in this_post.author.fans):
            pms = True
        elif (this_post.chat_mode == 1) and (user.user_id in this_post.author.friends):
            pms = True

        if pms:
            serializer = RepPostCommentCreateSerializer(data=request.data, author=user, main_cmt=main_cmt)
            if serializer.is_valid():
                serializer.save()
                this_post.comment_count += 1
                this_post.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "Unauthorized to perform this operation!"}, status=status.HTTP_403_FORBIDDEN)


class RepCommentLike(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_cmt(self, rep_cmt_id):
        try:
            return RepComment.objects.get(rep_cmt_id=rep_cmt_id)
        except RepComment.DoesNotExist:
            return Response({'error': "This comment dose not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, rep_cmt_id):
        this_cmt = self.get_cmt(rep_cmt_id)
        user = request.user
        if user.user_id in this_cmt.like_users:
            return Response({'status': 'Liked'})
        else:
            return Response({'status': "Don't like yet"})

    def patch(self, request, rep_cmt_id):
        this_cmt = self.get_cmt(rep_cmt_id)
        user = request.user
        temp = '@' + user.user_id
        if temp in this_cmt.like_users:
            temp_list = this_cmt.like_users.split(temp)
            this_cmt.like_users = ''.join(temp_list)
            this_cmt.save()
            return Response({'status': 'Unliked'})
        else:
            this_cmt.like_users += ('@' + user.user_id)
            this_cmt.save()
            return Response({'status': 'Liked'})
