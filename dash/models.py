from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.

class RunnerUser(models.Model):
    user = models.ForeignKey(User)
    display_name = models.CharField(max_length=100)
    oauth_key = models.CharField(max_length=255, blank=True, null=True, editable=False)
    email = models.EmailField()

class RunRecord(models.Model):
    user = models.ForeignKey(RunnerUser)
    distance = models.DecimalField(blank = False, decimal_places = 1, max_digits = 3)
    run_when = models.DateTimeField(blank = False)

def create_runner_user(sender, instance, created, **kwargs):
    if created:
        profile, created = RunnerUser.objects.get_or_create(user=instance)

post_save.connect(create_runner_user, sender=User)
