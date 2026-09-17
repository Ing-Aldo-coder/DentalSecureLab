from django.db import models
from patients.models import Patient


class MedicalRecord(models.Model):

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_record',
        verbose_name='Paciente'
    )

    reason = models.TextField(
        'Motivo de consulta'
    )

    diagnosis = models.TextField(
        'Diagnóstico',
        blank=True
    )

    treatment = models.TextField(
        'Tratamiento',
        blank=True
    )

    observations = models.TextField(
        'Observaciones',
        blank=True
    )

    created_at = models.DateTimeField(
        'Fecha de creación',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Última actualización',
        auto_now=True
    )

    def __str__(self):
        return f"Expediente de {self.patient}"

    class Meta:
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'


from auditlog.registry import auditlog
auditlog.register(MedicalRecord)