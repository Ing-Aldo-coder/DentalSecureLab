import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

DEFAULT_PASSWORD = "Clinica2026!"

USERS_DATA = [
    {
        "username": "admin",
        "first_name": "Administrador",
        "last_name": "General",
        "email": "admin@dentalsecurelab.local",
        "role": "admin",
        "is_superuser": True,
        "is_staff": True,
        "description": "Administrador General del Sistema / TI"
    },
    {
        "username": "dr_garcia",
        "first_name": "Dr. Roberto",
        "last_name": "García",
        "email": "r.garcia@dentalsecurelab.local",
        "role": "doctor",
        "is_superuser": False,
        "is_staff": False,
        "description": "Doctor Odontólogo General (Consultorio 1)"
    },
    {
        "username": "dr_martinez",
        "first_name": "Dr. Fernando",
        "last_name": "Martínez",
        "email": "f.martinez@dentalsecurelab.local",
        "role": "doctor",
        "is_superuser": False,
        "is_staff": False,
        "description": "Doctor Odontólogo General (Consultorio 2)"
    },
    {
        "username": "dra_lopez",
        "first_name": "Dra. Patricia",
        "last_name": "López",
        "email": "p.lopez@dentalsecurelab.local",
        "role": "doctor",
        "is_superuser": False,
        "is_staff": False,
        "description": "Doctora Odontóloga General (Consultorio 3)"
    },
    {
        "username": "dr_ramirez",
        "first_name": "Dr. Alejandro",
        "last_name": "Ramírez",
        "email": "a.ramirez@dentalsecurelab.local",
        "role": "doctor",
        "is_superuser": False,
        "is_staff": False,
        "description": "Especialista Odontológico - Ortodoncia (Consultorio 4)"
    },
    {
        "username": "dr_fernandez",
        "first_name": "Dr. Gonzalo",
        "last_name": "Fernández",
        "email": "g.fernandez@dentalsecurelab.local",
        "role": "doctor",
        "is_superuser": False,
        "is_staff": False,
        "description": "Especialista Odontológico - Endodoncia (Consultorio 4)"
    },
    {
        "username": "enfermero_carlos",
        "first_name": "Carlos",
        "last_name": "Mendoza",
        "email": "c.mendoza@dentalsecurelab.local",
        "role": "nurse",
        "is_superuser": False,
        "is_staff": False,
        "description": "Asistente Dental / Enfermero (Apoyo Clínico)"
    },
    {
        "username": "recepcion_ana",
        "first_name": "Ana",
        "last_name": "Morales",
        "email": "a.morales@dentalsecurelab.local",
        "role": "receptionist",
        "is_superuser": False,
        "is_staff": False,
        "description": "Recepcionista (Recepción y Citas)"
    }
]

def seed_users():
    print(f"[*] Inicializando plantilla clínica (8 personas) con contraseña por defecto: '{DEFAULT_PASSWORD}'\n")
    for data in USERS_DATA:
        username = data["username"]
        user, created = User.objects.get_or_create(username=username)
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.is_superuser = data["is_superuser"]
        user.is_staff = data["is_staff"]
        user.set_password(DEFAULT_PASSWORD)
        user.save()

        # Configurar perfil y rol
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = data["role"]
        profile.save()

        status = "CREADO" if created else "ACTUALIZADO"
        print(f"  - [{status}] Usuario: '{username:16}' | Rol: '{profile.get_role_display():32}' | Puesto: {data['description']}")

    print("\n[OK] Plantilla completa de 8 usuarios configurada exitosamente.")

if __name__ == "__main__":
    seed_users()
