from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    category=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# below was just for test---has no use in this project    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically adds the timestamp when submitted

    def __str__(self):
        return f"{self.name} - {self.email}"
