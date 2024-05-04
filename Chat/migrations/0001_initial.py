# Generated by Django 5.0.3 on 2024-04-17 15:01

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatBox',
            fields=[
                ('chat_box_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('members', models.TextField()),
                ('member_quantity', models.IntegerField(editable=False, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ChatBoxes',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('liked_user', models.TextField(blank=True, default='', null=True)),
                ('like_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_message', to='Chat.chatbox')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Message',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MessageImage',
            fields=[
                ('image_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/%Y/%m')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='Chat.message')),
            ],
            options={
                'db_table': 'Message_Images',
                'ordering': ['-created_at'],
            },
        ),
    ]