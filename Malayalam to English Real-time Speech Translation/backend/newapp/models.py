from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_receiver')

    class Meta:
        unique_together = ('sender', 'receiver')


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'favourites')
    favourite_user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} favourited {self.favourite_user}'
