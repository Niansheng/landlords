from datetime import datetime, timedelta
from properties.models import Contract


def notify_landlord():
    contracts = Contract.objects.all()
    now = datetime.now()
    notify_period = timedelta(days=14)
    for contract in contracts:
        delta = contract.end_date - now.date()
        if delta <= notify_period and delta > timedelta(days=0):
            send_email(contract)


def send_email(contract):
    # can have a better backends here
    text = "You need to find a new tenant"
    print(text, contract)
