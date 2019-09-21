from django.db import models
from apps.l_r.models import User
import datetime

class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors['destination'] = "Destination must be at least 3 characters"
        if len(postData['plan']) < 3:
            errors['plan'] = "Plan should be at least 3 characters"
        if postData['start_date'] > postData['end_date']:
            errors['bad_date_1'] = "End date is prior to start date"
        if postData['start_date'] < str(datetime.date.today()):
            errors['bad_date_2'] = "Start date must be in the future"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name="created_trips")
    joined_users = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    