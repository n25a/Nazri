from django.db import models

from ..user.models import CustomUser
from ..reason.models import Reason


class Penalty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    level = models.IntegerField(default=0)

    reason = models.ForeignKey(Reason)

    payed = models.BooleanField(default=False)

    create_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)
