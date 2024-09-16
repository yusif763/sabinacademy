from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, DailyPayments

@receiver(post_save, sender=DailyPayments)
def create_daily_payment(sender, instance, created, **kwargs):
    if created:
        Payment.objects.create(
            student=instance.student,
            course=instance.course,
            amount=instance.amount,
            cash_type = instance.cash_type
        )
