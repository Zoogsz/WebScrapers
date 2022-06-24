from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)  # Structured RSS Data
    link = models.CharField(max_length=2083, default= "", unique=True) # Article Link
    published = models.DateTimeField() # Published Date
    created_at = models.DateTimeField(auto_now_add=True) # Our data entery date
    update_at= models.DateTimeField(auto_now=True) # Updated at
    source = models.CharField(max_length=30, default="", blank=True, null=True) # Source

