from django.db import models
from User.models import User
from algorithm.base import formatDatetime
from django.core.validators import MinValueValidator

mode_choose = ((0, "Public"),
               (1, "Follower"),
               (2, "Fan"),
               (3, "Fiend"),
               (4, "Private"))


class Hashtag(models.Model):
    name = models.CharField(max_length=50)
    times_of_use = models.BigIntegerField(validators=[MinValueValidator(0)], default=1)

    objects = models.Manager()

    class Meta:
        db_table = 'Hashtag'
        ordering = ['-times_of_use']

    def __str__(self):
        return '#' + str(self.name)


class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    view_mode = models.IntegerField(choices=mode_choose, default=0)
    chat_mode = models.IntegerField(choices=mode_choose, default=0)
    caption = models.CharField(max_length=100, null=True, blank=True)
    hashtags = models.TextField(default='')
    like_users = models.TextField(null=True, blank=True, default="")
    like_count = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    comment_count = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Posts'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.like_count = len(str(self.like_users).split('@')[:-1])
        super().save(*args, **kwargs)

    def created_at_formatted(self):
        return formatDatetime(self.created_at)
    objects = models.Manager()


class Image(models.Model):
    image_id = models.BigAutoField(primary_key=True, editable=False)
    image = models.ImageField(upload_to='images/%Y/%m')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    objects = models.Manager()

    class Meta:
        abstract = True


class PostImage(Image):
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL, related_name='images')

    class Meta:
        db_table = 'Post_Images'
        ordering = ['-created_at']


class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    like_users = models.TextField(default='', null=True, blank=True)
    like_count = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = 'PostComments'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.like_count = len(str(self.like_users).split('@')[:-1])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content

    def created_at_formatted(self):
        return formatDatetime(self.created_at)


class RepComment(models.Model):
    rep_cmt_id = models.BigAutoField(primary_key=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main_cmt = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    like_users = models.TextField(default='', null=True, blank=True)
    like_count = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'PostRepComment'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.like_count = len(str(self.like_users).split('@')[:-1])
        super().save(*args, **kwargs)

    def created_at_formatted(self):
        return formatDatetime(self.created_at)
