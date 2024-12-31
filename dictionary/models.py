from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def upvotes(self):
        return self.votes.filter(vote_type='upvote').count()
    
    def downvotes(self):
        return self.votes.filter(vote_type='downvote').count()    

    def __str__(self):
        return self.title
    
class Example(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="examples")
    example_text = models.TextField()

    def __str__(self):
        return self.example_text

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'entry') # ensures only one vote per user