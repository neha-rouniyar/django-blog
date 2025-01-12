from django.db import models

class Blog(models.Model):
    title=models.CharField(max_length=255)
    author_name=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    description=models.TextField()
    author_email=models.CharField(max_length=255,null=True)
    author_dob=models.DateField(null=True)
    published_date=models.DateField(null=True)

    def __str__(self):
        return self.title