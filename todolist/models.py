from django.db import models

class Todo(models.Model):
    title=models.CharField(max_length=255,null=True)
    description=models.TextField(null=True)
    completed=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.title