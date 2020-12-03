import json
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from .managers import UserManager


class User(AbstractUser):
    gender = (
        ('F', "Female"),
        ('M', "Male"),
        ('NB', "Non-binary"),
    )
    level = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    gender = models.CharField(max_length=2, choices=gender, null=True)
    singles = models.BooleanField(null=True)
    doubles = models.BooleanField(null=True)
    mixed_doubles = models.BooleanField(null=True)
    picture = models.CharField(max_length=1000, null=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'level': str(self.level),
            'gender': self.gender,
            'singles': self.singles,
            'doubles': self.doubles,
            'mixed_double': self.mixed_doubles,
            'picture': self.picture
        }

    # objects = UserManager()


class Match(models.Model):
    game_types = (
        ('S', "Singles"),
        ('D', "Doubles"),
        ('MD', "Mixed Doubles"),
    )
    id = models.AutoField(primary_key=True, blank=True)
    match = models.ManyToManyField('User', related_name='match_group')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='match_created_by')
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=game_types)
    new = models.BooleanField(default=True)

    def clean(self, *args, **kwargs):
        if self.users.count() == 2 or self.users.count == 4:
            raise ValidationError("You can't assign more than four users to doubles group.")

    def serialize(self):
        return {
            'id': self.id,
            'match': [user.email for user in self.match.all()],
            'match_ids': [user.id for user in self.match.all()],
            'created_by': self.created_by.email,
            'created_date': self.created_date.strftime("%b %d %Y, %I:%M %p"),
            'type': self.type,
            'new': self.new
        }


class Message(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    text = models.TextField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='message_match')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_created_by')
    created_date = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'match': self.match.id,
            'created_by': self.created_by.email,
            'created_date': self.created_date.strftime("%b %d %Y, %I:%M %p")
        }
