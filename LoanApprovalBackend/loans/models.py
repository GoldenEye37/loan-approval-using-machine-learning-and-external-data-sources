import uuid
from django.db import models


# Create your models here.


class Trend_choice(models.TextChoices):
    """Trend choices. values => positive, negative, stable"""
    POSITIVE = 'positive', 'Positive'
    NEGATIVE = 'negative', 'Negative'
    STABLE = 'stable', 'Stable'


class MIS_Status(models.TextChoices):
    """MIS Status choices. values => "PIF", "CHGOFF" """
    PIF = 'PIF', 'Paid in Full'
    CHGOFF = 'CHGOFF', 'Charge off'


class Industry(models.Model):
    """Industry model."""
    industry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    trends = models.CharField(max_length=255, null=False, blank=False, choices=Trend_choice.choices,
                             default=Trend_choice.STABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.name} "


class Loan(models.Model):
    """Loan model."""
    loan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    company_name = models.CharField(max_length=255, null=False, blank=False)
    gross_approval = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField(max_length=50, null=False, blank=False)
    number_of_employees = models.IntegerField(null=False, blank=False)
    new_business = models.IntegerField(null=False, blank=False)
    urban = models.BooleanField(default=False, null=False, blank=False)
    industry = models.ForeignKey("loans.Industry", on_delete=models.DO_NOTHING, null=False, blank=False)
    mis_status = models.CharField(max_length=255,
                                  null=True, blank=True,
                                  choices=MIS_Status.choices,
                                  default=MIS_Status.PIF)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    # industry_trends = models.CharField(max_length=255,
    #                                    null=False, blank=False,
    #                                    choices=Trend_choice.choices,
    #                                    default=Trend_choice.STABLE)

    def __str__(self):
        return f"{self.name} "

