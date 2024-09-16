from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import DailyPayments

class Command(BaseCommand):
    help = 'Delete daily payments older than 5 days'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=5)
        old_payments = DailyPayments.objects.filter(payment_date__lt=threshold_date)
        old_payments.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {old_payments.count()} old daily payments'))
