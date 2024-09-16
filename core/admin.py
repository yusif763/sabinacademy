from django.contrib import admin
from .models import Teacher, Student, Course, Payment, NextPayments, DailyPayments
from .admin_site import admin_site  # Import the custom admin site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from datetime import datetime
from django.utils.html import format_html, mark_safe
from django.utils.timezone import now

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'phone', 'created_at', 'updated_at')
    search_fields = ('fullname', 'email', 'phone')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'grade', 'phone', 'teacher', 'amount', 'discount', 'final_amount', 'enterTime', 'startTime', 'created_at', 'updated_at')
    search_fields = ('fullname', 'phone', 'teacher__fullname')
    list_filter = ('teacher', 'grade')
    readonly_fields = ('payment_periods_display',)


    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [field for field in fields if field != 'payment_periods']

    def payment_periods_display(self, obj):
        if obj.payment_periods:
            dates = [f"<tr><td>{date}</td></tr>" for date in obj.payment_periods]
            return format_html("<table><thead><tr><th>Ödəniş Tarixi</th></tr></thead><tbody>{}</tbody></table>", mark_safe(''.join(dates)))
        return "Heç bir dövr yoxdur"

    payment_periods_display.short_description = 'Ödəniş Dövrləri'

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'created_at', 'updated_at')
    search_fields = ('student__fullname', 'course__name')
    list_filter = ('created_at',)

class NextPaymentsAdmin(admin.ModelAdmin):
    list_display = ('student', 'days_left', 'next_payment_date')
    search_fields = ('student__fullname',)
    list_filter = ('days_left', 'next_payment_date')

class DailyPaymentsAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'payment_date', 'cash_type')
    search_fields = ('student__fullname', 'course__name', 'cash_type')
    list_filter = ('payment_date', 'cash_type')

    def get_queryset(self, request):
        today = now().date()
        return super().get_queryset(request).filter(payment_date__date=today)

    def get_model_perms(self, request):
        if request.user.groups.filter(name='Reception').exists():
            return {}
        return super().get_model_perms(request)


admin_site.register(Teacher, TeacherAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Payment, PaymentAdmin)
admin_site.register(NextPayments, NextPaymentsAdmin)
admin_site.register(DailyPayments, DailyPaymentsAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)