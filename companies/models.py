from django.db import models

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=255, db_index=True)
    symbol = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    scripcode = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.company_name
