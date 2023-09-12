from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """create a topic within the journal that people can make entries for"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """create an entry for a specific topic that was created"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='entries')
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text

class Comment(models.Model):
    """comments on a certain topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='comments')
    comment = models.TextField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='comments')

    def __str__(self):
        return f"Comment by {self.owner} on {self.date_added}"


