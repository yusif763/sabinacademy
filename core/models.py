from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import datetime

COLOR_CHOICES = (
    ('CardToCard','Card To Card'),
    ('PostTerminal', 'Post Terminal'),
    ('Cash','Nəğd'),
)

class Teacher(models.Model):
    fullname = models.CharField(max_length=255, verbose_name="Tam Adı")
    email = models.EmailField(unique=True, verbose_name="E-poçt")
    phone = models.CharField(max_length=15, verbose_name="Telefon")
    courses = models.ManyToManyField('Course', related_name='teachers', verbose_name="Kurslar", null=True, blank=True)
    students = models.ManyToManyField('Student', related_name='assigned_teachers', blank=True, verbose_name="Tələbələr")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Müəllim"
        verbose_name_plural = "Müəllimlər"

class Student(models.Model):
    fullname = models.CharField(max_length=255, verbose_name="Tam Adı")
    grade = models.CharField(max_length=50, verbose_name="Sinif")
    phone = models.CharField(max_length=15, verbose_name="Telefon")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students_set', null=True, blank=True, verbose_name="Müəllim")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Məbləğ")
    discount = models.IntegerField(default=0, verbose_name="Endirim")
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Son Məbləğ", editable=False)
    enterTime = models.DateTimeField(verbose_name="Giriş Vaxtı" )
    payment_periods = models.JSONField(default=list, verbose_name="Ödəniş Dövrləri", blank=True)  # To store the generated payment periods
    startTime =  models.DateTimeField(verbose_name="Başlama Vaxtı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")

    def save(self, *args, **kwargs):
        self.calculate_final_amount()
        # Only generate payment periods if the instance is being created (not updated)
        if not self.id and self.enterTime and self.startTime:
            self.generate_payment_periods()
        super(Student, self).save(*args, **kwargs)

    def calculate_final_amount(self):
        self.final_amount = self.amount - self.discount

    def generate_payment_periods(self):
        payment_dates = []
        current_date = self.startTime

        for _ in range(12):  # Generate 12 months of payment dates
            payment_dates.append(current_date.strftime('%Y-%m-%dT%H:%M:%S'))
            # Move to the next month
            current_date += relativedelta(months=1)
        
        self.payment_periods = payment_dates
    def __str__(self):
        return self.fullname
    


    class Meta:
        verbose_name = "Tələbə"
        verbose_name_plural = "Tələbələr"
    
    

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kurs Adı")
    description = models.TextField(verbose_name="Kurs Təsviri")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments", verbose_name="Tələbə")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Məbləğ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")
    cash_type = models.CharField(max_length=20, choices=COLOR_CHOICES, verbose_name="Ödəniş Növü", null=True, blank=True)

    def __str__(self):
        return f"{self.student.fullname} - {self.course.name}"

    class Meta:
        verbose_name = "Ödəniş"
        verbose_name_plural = "Ödənişlər"

class NextPayments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Tələbə")
    days_left = models.IntegerField(verbose_name="Qalan Günlər")
    next_payment_date = models.DateField(verbose_name="Növbəti Ödəniş Tarixi")

    def __str__(self):
        return f"{self.student.fullname} - {self.days_left} gün qalıb"

    class Meta:
        verbose_name = "Növbəti Ödəniş"
        verbose_name_plural = "Növbəti Ödənişlər"

class DailyPayments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Tələbə")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Məbləğ")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Ödəniş Tarixi")
    cash_type = models.CharField(max_length=20, choices=COLOR_CHOICES, verbose_name="Ödəniş Növü", null=True, blank=True)


    def __str__(self):
        return f"{self.student.fullname} - {self.amount} AZN - {self.payment_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Gündəlik Ödəniş"
        verbose_name_plural = "Gündəlik Ödənişlər"
