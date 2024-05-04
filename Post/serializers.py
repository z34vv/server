from .models import Post, PostImage, Comment, Hashtag, RepComment
from rest_framework import serializers
from User.models import User
from User.serializers import UserSerializer


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image_id',
            'image',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    images = ImageSerializer(many=True, required=False)

    def __init__(self, author, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    class Meta:
        model = Post
        fields = ['post_id',
                  'author',
                  'view_mode',
                  'chat_mode',
                  'caption',
                  'hashtags',
                  'images',
                  'like_users',
                  'like_count',
                  'comment_count',
                  'created_at_formatted']

    def create(self, validated_data):
        hashtags = str(validated_data['hashtags']).split(' ')
        validated_data['author'] = self.author
        post = super().create(validated_data)
        if hashtags:
            for hashtag in hashtags:
                if hashtag[0] == '#':
                    hashtag = hashtag[1:]
                if Hashtag.objects.filter(name=hashtag):
                    this_hashtag = Hashtag.objects.get(name=hashtag)
                    this_hashtag.times_of_use += 1
                    this_hashtag.save()
                else:
                    Hashtag.objects.create(name=hashtag)
        return post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['post_id',
                  'author',
                  'view_mode',
                  'chat_mode',
                  'caption',
                  'hashtags',
                  'images',
                  'like_users',
                  'like_count',
                  'comment_count',
                  'created_at_formatted']

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance


class PostCommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    def __init__(self, author, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author
        self.post = post

    class Meta:
        model = Comment
        fields = ['comment_id',
                  'content',
                  'author',
                  'post',
                  'like_count',
                  'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.author
        validated_data['post'] = self.post
        comment = super().create(validated_data)
        return comment


class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ['comment_id',
                  'content',
                  'author',
                  'post',
                  'like_count',
                  'created_at']

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance


class RepPostCommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    main_cmt = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    def __init__(self, author, main_cmt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author
        self.main_cmt = main_cmt

    class Meta:
        model = RepComment
        fields = ['rep_cmt_id',
                  'content',
                  'author',
                  'main_cmt',
                  'like_count',
                  'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.author
        validated_data['main_cmt'] = self.main_cmt
        rep_cmt = super().create(validated_data)
        return rep_cmt


class RepPostCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    main_cmt = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)

    class Meta:
        model = RepComment
        fields = ['rep_cmt_id',
                  'content',
                  'author',
                  'main_cmt',
                  'like_count',
                  'created_at']

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance
