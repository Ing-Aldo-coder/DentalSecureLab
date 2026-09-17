from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from .models import LoginAttemptTracker


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


@ratelimit(key='ip', rate='15/m', method='POST', block=False)
def login_view(request):
    """
    Vista de autenticación protegida contra ataques de fuerza bruta y diccionario.
    Flujo de control progresivo:
    - Intento 1: Fallo inicial (error estándar, sin alerta de límite).
    - Intento 2 a 4: Alerta activa preventiva de límite con conteo de intentos restantes.
    - Intento 5: Bloqueo inmediato por 5 minutos (HTTP 429).
    - Reingreso tras 5 minutos: 2 intentos de gracia antes de bloqueo extendido por 30 minutos.
    - Éxito en cualquier paso: Reseteo automático a cero.
    """
    ip = get_client_ip(request)
    tracker, _ = LoginAttemptTracker.objects.get_or_create(ip_address=ip)
    now = timezone.now()

    # 1. Comprobación de estado de bloqueo activo
    is_blocked = False
    remaining_time_str = ""
    if tracker.blocked_until and now < tracker.blocked_until:
        is_blocked = True
        remaining_seconds = int((tracker.blocked_until - now).total_seconds())
        mins = (remaining_seconds // 60) + 1
        remaining_time_str = f"{mins} minuto{'s' if mins > 1 else ''}"
    elif tracker.blocked_until and now >= tracker.blocked_until:
        # Período de bloqueo finalizado: transición de fase
        tracker.blocked_until = None
        if tracker.stage == 0:
            tracker.stage = 1
            tracker.post_block_attempts = 0
            tracker.failed_attempts = 0
        elif tracker.stage == 2:
            tracker.stage = 1
            tracker.post_block_attempts = 0
            tracker.failed_attempts = 0
        tracker.save()

    # Si la IP está actualmente bloqueada
    if is_blocked:
        return render(
            request,
            'users/login.html',
            {
                'form': AuthenticationForm(),
                'is_blocked': True,
                'remaining_time': remaining_time_str,
                'block_stage': tracker.stage,
            },
            status=429
        )

    if request.user.is_authenticated:
        return redirect('dashboard')

    # 2. Manejo de formulario POST
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticación exitosa: Reseteo inmediato del contador
            tracker.failed_attempts = 0
            tracker.blocked_until = None
            tracker.stage = 0
            tracker.post_block_attempts = 0
            tracker.save()

            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            # Autenticación fallida (contraseña o usuario incorrectos)
            if tracker.stage >= 1:
                # Fase post-bloqueo de 5 minutos
                tracker.post_block_attempts += 1
                if tracker.post_block_attempts >= 2:
                    tracker.stage = 2
                    tracker.blocked_until = now + timedelta(minutes=30)
                    tracker.save()
                    return render(
                        request,
                        'users/login.html',
                        {
                            'form': AuthenticationForm(),
                            'is_blocked': True,
                            'remaining_time': "30 minutos",
                            'block_stage': 2,
                        },
                        status=429
                    )
                else:
                    tracker.save()
                    messages.error(request, "Contraseña incorrecta tras reactivación.")
                    return render(
                        request,
                        'users/login.html',
                        {
                            'form': form,
                            'show_alert': True,
                            'in_post_block': True,
                            'failed_attempts': tracker.post_block_attempts,
                            'remaining_attempts': 1,
                            'max_attempts': 2,
                        }
                    )
            else:
                # Fase normal inicial
                tracker.failed_attempts += 1
                if tracker.failed_attempts >= 5:
                    tracker.stage = 1
                    tracker.blocked_until = now + timedelta(minutes=5)
                    tracker.post_block_attempts = 0
                    tracker.save()
                    return render(
                        request,
                        'users/login.html',
                        {
                            'form': AuthenticationForm(),
                            'is_blocked': True,
                            'remaining_time': "5 minutos",
                            'block_stage': 1,
                        },
                        status=429
                    )
                elif tracker.failed_attempts >= 2:
                    tracker.save()
                    remaining = 5 - tracker.failed_attempts
                    messages.error(request, f"Contraseña incorrecta (Intento fallido {tracker.failed_attempts} de 5).")
                    return render(
                        request,
                        'users/login.html',
                        {
                            'form': form,
                            'show_alert': True,
                            'in_post_block': False,
                            'failed_attempts': tracker.failed_attempts,
                            'remaining_attempts': remaining,
                            'max_attempts': 5,
                        }
                    )
                else:
                    # Intento 1: Primer fallo (No mostrar la alerta de límite todavía)
                    tracker.save()
                    messages.error(request, "Credenciales de acceso incorrectas. Verifique usuario y contraseña.")
                    return render(
                        request,
                        'users/login.html',
                        {
                            'form': form,
                            'show_alert': False,
                            'failed_attempts': 1,
                        }
                    )

    # 3. Manejo de GET
    show_alert = False
    in_post_block = False
    failed_count = 0
    remaining_count = 5
    max_count = 5

    if tracker.stage >= 1 and tracker.post_block_attempts > 0:
        show_alert = True
        in_post_block = True
        failed_count = tracker.post_block_attempts
        remaining_count = max(0, 2 - tracker.post_block_attempts)
        max_count = 2
    elif tracker.stage == 0 and tracker.failed_attempts >= 2:
        show_alert = True
        in_post_block = False
        failed_count = tracker.failed_attempts
        remaining_count = max(0, 5 - tracker.failed_attempts)
        max_count = 5

    form = AuthenticationForm()
    return render(
        request,
        'users/login.html',
        {
            'form': form,
            'show_alert': show_alert,
            'in_post_block': in_post_block,
            'failed_attempts': failed_count,
            'remaining_attempts': remaining_count,
            'max_attempts': max_count,
            'is_blocked': False,
        }
    )


def logout_view(request):
    """Cierre de sesión seguro."""
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login')
