def create_monthly_payment_lines(sender, instance, created, **kwargs):
    if created:
        from apps.payments.models import MonthPaymentLine, Work

        works = Work.objects.filter(is_active=True)
        lines = []

        for work in works:
            lines.append(MonthPaymentLine(work=work, month=instance))

        MonthPaymentLine.objects.bulk_create(lines)
