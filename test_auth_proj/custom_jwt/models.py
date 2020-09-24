from django.db import models
from django.conf import settings


class Token(models.Model):

    access_token = models.TextField()
    access_token_expires = models.DateTimeField()

    refresh_token = models.TextField()
    refresh_token_expires = models.DateTimeField()

    active = models.BooleanField(default=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(fields=['access_token'], name='token'),
            models.constraints.UniqueConstraint(fields=['refresh_token'], name='refresh'),
        ]

    def __str__(self):
        return self.user.first_name
