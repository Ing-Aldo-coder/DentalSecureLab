from django.db import models
from patients.models import Patient


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Programada'),
        ('confirmed', 'Confirmada'),
        ('completed', 'Atendida'),
        ('cancelled', 'Cancelada'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Paciente'
    )

    date = models.DateField('Fecha')
    time = models.TimeField('Hora')
    reason = models.CharField('Motivo de la consulta', max_length=200)

    status = models.CharField(
        'Estado',
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    notes = models.TextField('Observaciones', blank=True)

    created_at = models.DateTimeField(
        'Fecha de registro',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient} - {self.date} {self.time}"

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['date', 'time']