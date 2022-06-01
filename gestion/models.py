from django.db import models
import uuid
from users.models import Patient, Facility


# Create your models here.

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    date = models.DateTimeField(max_length=60,null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    Description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "order " + self.id
