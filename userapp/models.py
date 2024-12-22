from django.db import models

class Blog(models.Model):
    title=models.CharField(max_length=255)
    author_name=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    description=models.TextField()

    def __str__(self):
        return self.title