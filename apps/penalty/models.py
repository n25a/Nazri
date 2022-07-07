from django.db import models
from ..user.models import CustomUser
from ..reason.models import Reason


class Penalty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    rate = models.IntegerField(default=0)

    reason = models.ForeignKey(Reason)

    create_at = models.DateTimeField(auto_now_add=True)
