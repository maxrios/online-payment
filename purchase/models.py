from django.db import models
from user.models import Profile


class Purchase(models.Model):
    purchase_id         = models.CharField(max_length=100)
    date                = models.DateTimeField(auto_now=True)
    profile             = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='purchases_info')
    