from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def login_view(request):
    """
    Vista de autenticación protegida contra ataques de fuerza bruta y diccionario.
    Aplica una restricción máxima de 5 peticiones POST por minuto por dirección IP.
    """
    if getattr(request, 'limited', False):
        messages.error(
            request,
            "Alerta de Seguridad: Demasiados intentos fallidos desde su dirección IP. "
            "El acceso ha sido bloqueado temporalmente por 1 minuto para mitigar ataques de fuerza bruta."
        )
        return render(
            request,
            'users/login.html',
            {'form': AuthenticationForm(), 'rate_limited': True},
            status=429
        )

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Credenciales de acceso incorrectas. Verifique usuario y contraseña.")
    else:
        form = AuthenticationForm()

    return render(
        request,
        'users/login.html',
        {'form': form}
    )


def logout_view(request):
    """Cierre de sesión seguro."""
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login')
