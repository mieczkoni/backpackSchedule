from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


# Create your models here.
class Subject(models.Model):
    """Model representing a subject."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a subject.')
    name = models.CharField(max_length=300)
    hours = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class SubjectRating(models.Model):
    """Model representing a subject ratings"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    subject_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hours = models.IntegerField(default=0)
    rated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
