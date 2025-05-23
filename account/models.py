from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.request_user} following {self.followed_user}'    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)