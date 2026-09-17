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
