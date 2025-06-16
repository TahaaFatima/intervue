from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class InterviewEntry(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    date        = models.DateField()
    job_title   = models.CharField(max_length=100)
    company     = models.CharField(max_length=100)
    description = models.TextField()
    resume      = models.FileField(upload_to='resumes/', null=True, blank=True)
    questions   = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company} on {self.date}"