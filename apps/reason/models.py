from django.db import models


class Reason(models.Model):
    reason = models.CharField(max_length=100, blank=False)

    create_at = models.DateTimeField(auto_now_add=True)
