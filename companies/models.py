from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=255, db_index=True)
    symbol = models.CharField(max_length=50, null=True,
                              blank=True, db_index=True)
    scripcode = models.CharField(max_length=50, null=True, blank=True)
    co_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.company_name


class CompanyMetrics(models.Model):
    company = models.OneToOneField(
        Company, to_field='co_code', on_delete=models.CASCADE, related_name='metrics'
    )
    pe = models.FloatField(null=True, blank=True)
    roe_ttm = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Metrics for {self.company.company_name}"
