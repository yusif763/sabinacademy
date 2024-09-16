from celery import shared_task
from .models import Student, NextPayments, DailyPayments
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
from django.core.mail import EmailMessage
from io import BytesIO
from .models import NextPayments
from django.utils import timezone
from datetime import datetime

@shared_task
def update_next_payments():
    NextPayments.objects.all().delete()
    today = timezone.now().date()

    for student in Student.objects.all():
        for payment_date in student.payment_periods:
            payment_date = timezone.make_aware(datetime.strptime(payment_date, '%Y-%m-%dT%H:%M:%S'))
            days_left = (payment_date.date() - today).days

            if 0 <= days_left <= 5:
                NextPayments.objects.create(
                    student=student,
                    days_left=days_left,
                    next_payment_date=payment_date.date()
                )

@shared_task
def update_daily_payments():
    five_days_ago = timezone.now() - timedelta(days=5)
    DailyPayments.objects.filter(payment_date__lt=five_days_ago).delete()

@shared_task
def send_next_payments_report():
    # Fetch students with 5 days or fewer left for their next payment
    next_payments = NextPayments.objects.all()
    
    if not next_payments:
        return  # No data to report

    # Create a Pandas DataFrame from the query
    data = {
        'Student': [np.student.fullname for np in next_payments],
        'Days Left': [np.days_left for np in next_payments],
        'Next Payment Date': [np.next_payment_date for np in next_payments],
    }
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Next Payments', index=False)
    excel_file.seek(0)

    # Prepare the email
    email = EmailMessage(
        subject='Next Payments Report',
        body='Please find the attached report for students with 5 days or fewer left before their next payment.',
        from_email='your_email@example.com',
        to=['yuseefhuseynli@gmail.com'],
    )
    email.attach('next_payments_report.xlsx', excel_file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()