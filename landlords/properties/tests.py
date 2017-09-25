from datetime import datetime, timedelta
from freezegun import freeze_time
from mock import patch

from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


from properties.models import Contract, Estate
from properties.notify_landlord import notify_landlord


class PropertiesAppTest(TestCase):
    @classmethod
    def setUp(self):
        landlord = Group.objects.get(name='landlord')
        tenant = Group.objects.get(name='tenant')
        self.landlord = User.objects.create(username='John')
        self.landlord.groups.add(landlord)
        self.tenant = User.objects.create(username='Peter')
        self.tenant.groups.add(tenant)

        self.house = Estate.objects.create(
            name='Lemon house',
            address='18 lemon street',
            postcode='NE14 2AP',
            owner=self.landlord
        )
        now = datetime(2017, 9, 1)
        self.contract = Contract.objects.create(
            tenant=self.tenant,
            estate=self.house,
            start_date=now,
            end_date=now + timedelta(days=30)
        )

    @freeze_time('2017-09-01')
    def test_contract_conflict(self):
        now = datetime.now().date()
        days10 = timedelta(days=10)
        with self.assertRaises(ValidationError):
            Contract.objects.create(
                tenant=self.tenant,
                estate=self.house,
                start_date=now - days10,
                end_date=now + days10
            )

        with self.assertRaises(ValidationError):
            Contract.objects.create(
                tenant=self.tenant,
                estate=self.house,
                start_date=now + days10,
                end_date=now + timedelta(days=60)
            )

        with self.assertRaises(ValidationError):
            Contract.objects.create(
                tenant=self.tenant,
                estate=self.house,
                start_date=now + days10,
                end_date=now - days10
            )

    @freeze_time('2017-09-25')
    @patch('properties.notify_landlord.send_email')
    def test_notify_landlord(self, mock):
        now = datetime(2017, 10, 5)
        Contract.objects.create(
            tenant=self.tenant,
            estate=self.house,
            start_date=now,
            end_date=now + timedelta(days=30)
        )
        notify_landlord()
        self.assertTrue(mock.call_count, 1)
