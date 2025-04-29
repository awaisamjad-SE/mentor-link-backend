from django.db import models
from django.conf import settings
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_teacher_reply = models.BooleanField(default=False)

    # NEW FIELDS
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.message[:30]}..."

    def mark_as_read(self):
        self.read = True
        self.read_at = timezone.now()
        self.save(update_fields=["read", "read_at"])
