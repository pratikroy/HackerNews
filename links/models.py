from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Link(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True, editable=False)
    upvotes = models.ManyToManyField(User, related_name='votes')

class Comment(models.Model):
    body = models.TextField()
    commented_on = models.ForeignKey(Link, on_delete=models.CASCADE)
    in_reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
