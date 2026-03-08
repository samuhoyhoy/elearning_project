from django.db import models
from users.models import UserProfile

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # who sent the message
    content = models.TextField()                                      # message text
    timestamp = models.DateTimeField(auto_now_add=True)               # time sent

    def __str__(self):
        return f"{self.sender.real_name}: {self.content[:30]}"
