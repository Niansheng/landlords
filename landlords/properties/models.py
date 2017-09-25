from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q


class Estate(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'tenant'})

    def __str__(self):
        return '{}: {}'.format(self.name, self.address)


class Contract(models.Model):
    tenant = models.ForeignKey(
        User,
        limit_choices_to={'groups__name': 'tenant'})
    estate = models.ForeignKey(Estate)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['end_date']

    def __str__(self):
        return '{} has contract from {} to {} in {}'.format(
            self.tenant.username, self.start_date, self.end_date, self.estate
        )

    def validate_unique(self, **kwargs):
        """Only one contract for one estate at a period of time
        """

        contract = Contract.objects.filter(
            Q(estate=self.estate),
            Q(
                start_date__lte=self.start_date,
                end_date__gte=self.start_date
            ) | Q(
                start_date__lte=self.end_date,
                end_date__gte=self.end_date
            ),
        )

        if contract:
            raise ValidationError(
                'This property is occupied from {} to {} by {}'.format(
                    contract[0].start_date,
                    contract[0].end_date,
                    contract[0].tenant
                )
            )
        else:
            return super().validate_unique(**kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
