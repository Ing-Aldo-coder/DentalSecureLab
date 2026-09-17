from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador del Sistema'),
        ('doctor', 'Doctor Odontólogo / Especialista'),
        ('nurse', 'Asistente Dental / Enfermero'),
        ('receptionist', 'Recepcionista'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    role = models.CharField(
        'Rol de Sistema',
        max_length=20,
        choices=ROLE_CHOICES,
        default='doctor'
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'


class LoginAttemptTracker(models.Model):
    """
    Control progresivo de intentos de autenticación y mitigación de fuerza bruta.
    - Intentos 1 a 4: Conteo progresivo con advertencia activa a partir del intento 2.
    - Intento 5: Bloqueo temporal inmediato por 5 minutos.
    - Reincidencia post-bloqueo: 2 intentos de gracia antes de bloqueo extendido por 30 minutos.
    - Éxito en cualquier paso: Reseteo total inmediato a cero.
    """
    ip_address = models.CharField('Dirección IP', max_length=45, unique=True)
    failed_attempts = models.PositiveIntegerField('Intentos Fallidos', default=0)
    blocked_until = models.DateTimeField('Bloqueado Hasta', null=True, blank=True)
    stage = models.PositiveSmallIntegerField('Fase de Bloqueo', default=0) # 0: Normal, 1: Post 5min, 2: Bloqueo 30min
    post_block_attempts = models.PositiveIntegerField('Intentos Post-Bloqueo', default=0)
    last_attempt_at = models.DateTimeField('Último Intento', auto_now=True)

    class Meta:
        verbose_name = 'Control de Intentos de Login'
        verbose_name_plural = 'Controles de Intentos de Login'

    def __str__(self):
        return f"{self.ip_address} (Fallos: {self.failed_attempts}, Fase: {self.stage})"


def get_user_role(self):
    """Devuelve el rol del usuario garantizando compatibilidad con RBAC."""
    if hasattr(self, 'profile') and self.profile and self.profile.role:
        return self.profile.role
    if self.is_superuser:
        return 'admin'
    return getattr(self, '_role', 'doctor')


if not hasattr(User, 'role'):
    User.role = property(get_user_role)


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'admin' if instance.is_superuser else 'doctor'
        UserProfile.objects.create(user=instance, role=role)
    elif hasattr(instance, 'profile'):
        instance.profile.save()
