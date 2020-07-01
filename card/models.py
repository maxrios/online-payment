from django.db import models
from user.models import Profile

class Cards(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cards_info')
    card_id = models.CharField(max_length=100)
