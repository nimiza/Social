from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta():
        ordering = ['-created']


    def __str__(self):
        return f'{self.slug} - {self.created}'
    
    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.id, self.slug])
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', null=True, blank=True)
    is_reply = models.BooleanField(default=False)

    class Meta():
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} - {self.body[:20]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')


    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
    