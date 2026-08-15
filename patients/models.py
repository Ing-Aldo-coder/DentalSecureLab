from django.db import models


class Patient(models.Model):
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellidos", max_length=150)
    birth_date = models.DateField("Fecha de nacimiento")
    phone = models.CharField("Teléfono", max_length=20, blank=True)
    email = models.EmailField("Correo electrónico", blank=True)
    address = models.TextField("Dirección", blank=True)

    created_at = models.DateTimeField("Fecha de registro", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["last_name", "first_name"]
