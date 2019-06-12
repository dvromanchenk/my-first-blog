from django.db import models


class Chat(models.Model):
    theme = models.CharField(max_length=50)

    def __str__(self):
        return self.theme


class ChatMessage(models.Model):
    message = models.CharField(max_length=150)
    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE)

    def __str__(self):
        return self.theme