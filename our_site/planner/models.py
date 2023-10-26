from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #roles = models.ManyToManyField("Role", related_name="fulfilled_by")
    def __str__(self):
        return self.user


class Event(models.Model):
    user = models.ForeignKey(User, related_name="planner", on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=30)
    date = models.DateField()
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    invitees = models.ManyToManyField(Profile, related_name="invitations")
    def __str__(self):
        return (
            f"{self.owner} "
            f"{self.name[:30]}... "
            f"({self.date:%Y-%m-%d %H:%M}): "
            f"{self.description[:200]}... "
            f"{self.location[:50]}..."
            f"{self.invitees}"
        )
    

class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="roles")
    amount = models.IntegerField()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

