from django.db import models
from patients.models import Patient


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Paciente'
    )

    date = models.DateField('Fecha')

    concept = models.CharField(
        'Concepto',
        max_length=200
    )

    amount = models.DecimalField(
        'Monto',
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        'Método de pago',
        max_length=20,
        choices=PAYMENT_METHODS
    )

    notes = models.TextField(
        'Observaciones',
        blank=True
    )

    created_at = models.DateTimeField(
        'Fecha de registro',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient} - ${self.amount}"

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-date']