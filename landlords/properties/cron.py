import kronos

from properties.notify_landlord import notify_landlord


@kronos.register('0 0 * * *')
def notify():
    print('Checking contract and notify landlords')
    notify_landlord()
