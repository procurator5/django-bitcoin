from django.core.management.base import BaseCommand
from django_bitcoin.models import Wallet


class Command(BaseCommand):
    help = """fix balances
"""

    def handle(self, **options):
        print("starting...")
        for w in Wallet.objects.all():
            w.last_balance = w.total_balance()
            w.save()



