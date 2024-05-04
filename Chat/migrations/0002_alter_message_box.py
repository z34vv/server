# Generated by Django 5.0.3 on 2024-04-17 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='box',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_message', to='Chat.chatbox'),
        ),
    ]
