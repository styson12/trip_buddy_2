from django.db import models
from apps.t_b.models import *
import re
import bcrypt

#L_R

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']) or postData['email'] in User.objects.values_list('email', flat=True):            
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirm_pw']:
            errors['password_missmatch'] = "Passwords don't match"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        return errors 

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
