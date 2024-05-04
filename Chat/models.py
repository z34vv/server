from django.db import models
from Post.models import Image
from User.models import User
from algorithm.base import formatDatetime
from django.core.validators import MinValueValidator


class ChatBox(models.Model):
    chat_box_id = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    members = models.TextField()
    member_quantity = models.IntegerField(validators=[MinValueValidator(0)], editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = 'ChatBoxes'

    def save(self, *args, **kwargs):
        self.member_quantity = len(str(self.members).split('@')[1:])
        super(self).save(*args, **kwargs)

    def __str__(self):
        if self.name is None:
            member = str(self.members).split('@')
            name = f"{member[0]}, {member[1]} and {str(self.member_quantity - 2)} other members"
            return name
        return self.name


class Message(models.Model):
    message_id = models.BigAutoField(primary_key=True, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    box = models.ForeignKey(ChatBox, on_delete=models.CASCADE, related_name='chat_message', null=True, blank=True)

    content = models.TextField()
    is_read = models.BooleanField(default=False)
    liked_user = models.TextField(default='', null=True, blank=True)
    like_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']
        db_table = "Message"

    def save(self, *args, **kwargs):
        self.like_quantity = len(str(self.liked_user).split('@')[1:])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    def created_at_formatted(self):
        return formatDatetime(self.created_at)


class MessageImage(Image):
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL, related_name='images')

    class Meta:
        db_table = 'Message_Images'
        ordering = ['-created_at']
