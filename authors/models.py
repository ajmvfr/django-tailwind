from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Book author class
    Managed only in the django admin
    """
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name}"
    
    