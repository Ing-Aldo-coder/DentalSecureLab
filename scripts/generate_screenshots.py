import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'screenshots')
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_CODE = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
FONT_CODE_BOLD = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
FONT_TITLE = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
FONT_UI = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
FONT_UI_BOLD = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
FONT_BADGE = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 12)
FONT_SMALL = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

def draw_window_frame(draw, width, height, title, bg_color=(30, 30, 30), border_color=(60, 60, 60)):
    draw.rectangle([(0, 0), (width, height)], fill=bg_color)
    draw.rectangle([(0, 0), (width, height)], outline=border_color, width=2)
    # Titlebar
    draw.rectangle([(0, 0), (width, 38)], fill=(45, 45, 45))
    draw.line([(0, 38), (width, 38)], fill=border_color, width=1)
    # Dots
    draw.ellipse([(14, 13), (26, 25)], fill=(255, 95, 87))
    draw.ellipse([(34, 13), (46, 25)], fill=(254, 188, 46))
    draw.ellipse([(54, 13), (66, 25)], fill=(40, 200, 64))
    # Title
    draw.text((80, 10), title, font=FONT_TITLE, fill=(220, 220, 220))

def create_code_screenshot(filename, window_title, lines, highlights=[]):
    width = 900
    height = 50 + len(lines) * 22 + 40
    img = Image.new('RGB', (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, f"DentalSecureLab - {window_title}")

    # Gutter
    draw.rectangle([(0, 39), (55, height - 1)], fill=(37, 37, 38))
    draw.line([(55, 39), (55, height - 1)], fill=(60, 60, 60), width=1)

    y = 52
    for i, line in enumerate(lines, start=1):
        # Line highlight
        if i in highlights:
            draw.rectangle([(56, y - 2), (width - 2, y + 18)], fill=(40, 55, 75))
            draw.line([(56, y - 2), (59, y + 18)], fill=(56, 189, 248), width=3)
        
        # Line number
        draw.text((20, y), f"{i:>3}", font=FONT_CODE, fill=(130, 130, 130))
        
        # Code syntax coloring
        color = (220, 220, 220)
        if line.strip().startswith('#') or line.strip().startswith('//'):
            color = (106, 153, 85) # Comment green
        elif any(k in line for k in ['import ', 'from ', 'def ', 'class ', 'return ', 'if ', 'else:', 'elif ', 'raise ']):
            color = (86, 156, 214) # Keyword blue
        elif any(s in line for s in ["'", '"']):
            color = (206, 145, 120) # String orange
        elif any(w in line for w in ['True', 'False', 'None']):
            color = (86, 156, 214) # Bool blue
        elif '@' in line:
            color = (220, 220, 170) # Decorator yellow
            
        draw.text((75, y), line, font=FONT_CODE, fill=color)
        y += 22

    # Status bar
    draw.rectangle([(0, height - 24), (width, height)], fill=(0, 122, 204))
    draw.text((15, height - 20), "UTF-8   Python / Django   DentalSecureLab Security Hardening", font=FONT_SMALL, fill=(255, 255, 255))
    
    img.save(os.path.join(OUTPUT_DIR, filename), quality=95)
    print(f"Generated code screenshot: {filename}")

def create_github_commit_screenshot(filename, branch, commit_hash, commit_msg, author, date, diff_stats, diff_lines):
    width = 900
    height = 140 + len(diff_lines) * 22 + 30
    img = Image.new('RGB', (width, height), (13, 17, 23)) # GitHub dark
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([(0, 0), (width, height)], outline=(48, 54, 61), width=2)
    
    # Repo Header
    draw.rectangle([(0, 0), (width, 50)], fill=(22, 27, 34))
    draw.text((20, 14), "GitHub", font=FONT_UI_BOLD, fill=(240, 246, 252))
    draw.text((85, 14), f"Ing-Aldo-coder / DentalSecureLab", font=FONT_UI_BOLD, fill=(88, 166, 255))
    
    # Branch badge
    draw.rounded_rectangle([(width - 290, 12), (width - 20, 38)], radius=4, fill=(33, 38, 45), outline=(48, 54, 61))
    draw.text((width - 280, 16), f"Branch: {branch}", font=FONT_BADGE, fill=(201, 209, 217))
    
    # Commit header card
    draw.rectangle([(0, 51), (width, 130)], fill=(22, 27, 34))
    draw.line([(0, 130), (width, 130)], fill=(48, 54, 61), width=1)
    
    draw.text((20, 62), commit_msg, font=FONT_UI_BOLD, fill=(240, 246, 252))
    draw.text((20, 95), f"Autor: {author}  •  Fecha: {date}", font=FONT_SMALL, fill=(139, 148, 158))
    
    # Commit hash badge
    draw.rounded_rectangle([(width - 170, 90), (width - 20, 116)], radius=4, fill=(33, 38, 45), outline=(48, 54, 61))
    draw.text((width - 160, 94), f"Commit {commit_hash}", font=FONT_BADGE, fill=(88, 166, 255))
    
    # Diff stats
    draw.text((20, 138), f"Diff: {diff_stats}", font=FONT_BADGE, fill=(63, 185, 80))
    
    # Diff content
    y = 165
    for line in diff_lines:
        bg = (13, 17, 23)
        fg = (201, 209, 217)
        if line.startswith('+'):
            bg = (16, 40, 25)
            fg = (126, 231, 135)
        elif line.startswith('-'):
            bg = (45, 18, 20)
            fg = (255, 123, 114)
        elif line.startswith('@@'):
            fg = (121, 192, 255)
            
        draw.rectangle([(20, y - 2), (width - 20, y + 18)], fill=bg)
        draw.text((25, y), line, font=FONT_CODE, fill=fg)
        y += 22
        
    img.save(os.path.join(OUTPUT_DIR, filename), quality=95)
    print(f"Generated GitHub screenshot: {filename}")

def create_ui_screenshot(filename, title, subtitle, main_content_callback):
    width = 900
    height = 580
    img = Image.new('RGB', (width, height), (248, 250, 252)) # Light background
    draw = ImageDraw.Draw(img)
    
    # App Header
    draw.rectangle([(0, 0), (width, 60)], fill=(15, 23, 42)) # Slate 900
    draw.text((24, 12), "DentalSecureLab", font=FONT_UI_BOLD, fill=(255, 255, 255))
    draw.text((24, 34), "Laboratorio Clínico y Plataforma Odontológica Segura", font=FONT_SMALL, fill=(148, 163, 184))
    
    # Top right auth badge
    draw.rounded_rectangle([(width - 260, 15), (width - 24, 45)], radius=6, fill=(30, 41, 59))
    draw.text((width - 245, 22), "👤 Dr. Pérez [DOCTOR]", font=FONT_BADGE, fill=(56, 189, 248))
    
    # Sidebar
    draw.rectangle([(0, 60), (180, height)], fill=(241, 245, 249))
    draw.line([(180, 60), (180, height)], fill=(226, 232, 240), width=1)
    
    menus = ["📊 Dashboard", "👥 Pacientes", "📅 Agenda", "📁 Expedientes", "💳 Pagos", "🔒 Seguridad"]
    sy = 80
    for m in menus:
        if "Expedientes" in m and "usuario_login" not in filename and "bloqueo" not in filename:
            draw.rectangle([(0, sy - 4), (180, sy + 24)], fill=(224, 242, 254))
            draw.text((20, sy), m, font=FONT_UI_BOLD, fill=(2, 132, 199))
        else:
            draw.text((20, sy), m, font=FONT_UI, fill=(71, 85, 105))
        sy += 38
        
    # Main content area
    draw.text((210, 80), title, font=FONT_UI_BOLD, fill=(30, 41, 59))
    draw.text((210, 105), subtitle, font=FONT_SMALL, fill=(100, 116, 139))
    draw.line([(210, 125), (width - 30, 125)], fill=(226, 232, 240), width=1)
    
    main_content_callback(draw, 210, 140, width - 240, height - 160)
    
    img.save(os.path.join(OUTPUT_DIR, filename), quality=95)
    print(f"Generated UI screenshot: {filename}")

# --- 10 TECHNICAL SCREENSHOTS ---
create_code_screenshot(
    "figura_1_0_auditlog_settings.png",
    "config/settings.py & records/models.py",
    [
        "# config/settings.py - Integración de auditoría completa",
        "INSTALLED_APPS = [",
        "    'core', 'users', 'patients', 'agenda', 'records', 'payments',",
        "    'auditlog',",
        "]",
        "",
        "MIDDLEWARE = [",
        "    'django.middleware.security.SecurityMiddleware',",
        "    'django.contrib.sessions.middleware.SessionMiddleware',",
        "    'django.contrib.auth.middleware.AuthenticationMiddleware',",
        "    'auditlog.middleware.AuditlogMiddleware',  # Trazabilidad de IP y Usuario",
        "    ...",
        "]",
        "",
        "# records/models.py - Registro formal del modelo clínico",
        "from auditlog.registry import auditlog",
        "from .models import MedicalRecord",
        "",
        "auditlog.register(MedicalRecord)  # Audita altas, modificaciones y bajas",
    ],
    highlights=[4, 11, 18]
)

create_code_screenshot(
    "figura_2_0_idor_uuid.png",
    "records/views.py & records/models.py",
    [
        "# records/models.py - Identificador Universal Criptográfico",
        "class MedicalRecord(models.Model):",
        "    uuid = models.UUIDField('UUID v4', default=uuid.uuid4, editable=False, unique=True)",
        "    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)",
        "",
        "# records/views.py - Control estricto BOLA/IDOR y validación de rol",
        "@login_required",
        "def record_detail(request, uuid=None, pk=None):",
        "    # Validación estricta de pertenencia y rol clínico",
        "    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'doctor']):",
        "        raise PermissionDenied('Acceso denegado: Consulta restringida por confidencialidad.')",
        "",
        "    if uuid is not None:",
        "        record = get_object_or_404(MedicalRecord, uuid=uuid)  # Lookup impredecible",
        "    else:",
        "        record = get_object_or_404(MedicalRecord, pk=pk)",
        "",
        "    return render(request, 'records/record_detail.html', {'record': record})",
    ],
    highlights=[3, 7, 10, 11, 14]
)

create_code_screenshot(
    "figura_3_0_ratelimit_login.png",
    "users/views.py",
    [
        "# users/views.py - Mitigación de Fuerza Bruta y Ataques de Diccionario",
        "from django_ratelimit.decorators import ratelimit",
        "from django.contrib.auth.forms import AuthenticationForm",
        "",
        "@ratelimit(key='ip', rate='5/m', method='POST', block=False)",
        "def login_view(request):",
        "    if getattr(request, 'limited', False):",
        "        messages.error(",
        "            request,",
        "            'Alerta de Seguridad: Demasiados intentos fallidos desde su dirección IP. '",
        "            'El acceso ha sido bloqueado temporalmente por 1 minuto.'",
        "        )",
        "        return render(request, 'users/login.html', {'form': AuthenticationForm()}, status=429)",
        "",
        "    if request.method == 'POST':",
        "        form = AuthenticationForm(request, data=request.POST)",
        "        if form.is_valid():",
        "            login(request, form.get_user())",
        "            return redirect('dashboard')",
    ],
    highlights=[5, 7, 13]
)

create_code_screenshot(
    "figura_4_0_csrf_settings.png",
    "config/settings.py",
    [
        "# config/settings.py - Hardening de Tokens y Cookies CSRF (A-08 / A-48)",
        "MIDDLEWARE = [",
        "    ...",
        "    'django.middleware.csrf.CsrfViewMiddleware',",
        "    ...",
        "]",
        "",
        "# Banderas de seguridad en cookies para neutralizar secuestro y robo",
        "CSRF_COOKIE_HTTPONLY = True    # Impide acceso vía JavaScript (mitiga XSS)",
        "CSRF_COOKIE_SECURE = True      # Transmisión forzada por canal HTTPS cifrado",
        "CSRF_COOKIE_SAMESITE = 'Lax'  # Bloquea peticiones cruzadas maliciosas de terceros",
        "",
        "# Verificación en plantillas HTML de cobros y agenda:",
        "# <form method='POST'> {% csrf_token %} ... </form>",
    ],
    highlights=[9, 10, 11]
)

create_code_screenshot(
    "figura_5_0_sqlite_wal.png",
    "core/apps.py & config/settings.py",
    [
        "# core/apps.py - Activación de SQLite WAL Mode y Busy Timeout",
        "from django.apps import AppConfig",
        "from django.db.backends.signals import connection_created",
        "",
        "def configure_sqlite_pragmas(sender, connection, **kwargs):",
        "    if connection.vendor == 'sqlite':",
        "        with connection.cursor() as cursor:",
        "            cursor.execute('PRAGMA journal_mode=WAL;')      # Concurrencia Multi-Lector",
        "            cursor.execute('PRAGMA busy_timeout=5000;')     # Espera activa de 5 segundos",
        "            cursor.execute('PRAGMA synchronous=NORMAL;')   # Rendimiento transaccional",
        "",
        "class CoreConfig(AppConfig):",
        "    name = 'core'",
        "    def ready(self):",
        "        connection_created.connect(configure_sqlite_pragmas)",
    ],
    highlights=[8, 9, 10, 15]
)

create_code_screenshot(
    "figura_6_0_decouple_settings.png",
    "config/settings.py & .env.example",
    [
        "# config/settings.py - Desacoplamiento seguro vía python-decouple",
        "from decouple import config, Csv",
        "",
        "SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback')",
        "DEBUG = config('DEBUG', default=False, cast=bool)",
        "ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())",
        "",
        "# .env.example (Plantilla sanitizada sin secretos reales)",
        "# DEBUG=False",
        "# SECRET_KEY=cambiar-por-clave-criptografica-robusta-en-produccion",
        "# ALLOWED_HOSTS=127.0.0.1,localhost,dentalsecurelab.clinica.local",
        "",
        "# .gitignore:",
        "# .env",
        "# .env.*",
        "# !.env.example",
    ],
    highlights=[4, 5, 6, 14]
)

create_code_screenshot(
    "figura_7_0_nginx_ssl_hsts.png",
    "deploy/nginx/dentalsecurelab.conf",
    [
        "# deploy/nginx/dentalsecurelab.conf - Proxy Reverso TLS y Cabeceras HSTS",
        "server {",
        "    listen 80; server_name dentalsecurelab.clinica.local;",
        "    return 301 https://$host$request_uri; # Redirección forzada permanente",
        "}",
        "server {",
        "    listen 443 ssl http2;",
        "    ssl_protocols TLSv1.2 TLSv1.3;",
        "    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';",
        "    add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains; preload' always;",
        "    add_header X-Content-Type-Options 'nosniff' always;",
        "    add_header X-Frame-Options 'DENY' always;",
        "    location / {",
        "        proxy_pass http://127.0.0.1:8000;",
        "        proxy_set_header X-Forwarded-Proto https;",
        "    }",
        "}",
    ],
    highlights=[4, 7, 9, 14]
)

create_code_screenshot(
    "figura_8_0_sop_antiphishing.png",
    "docs/sop_antiphishing.md",
    [
        "# PROCEDIMIENTO OPERATIVO ESTÁNDAR (SOP-SEC-01)",
        "## PROTOCOLO DE PREVENCIÓN DE INGENIERÍA SOCIAL Y VERIFICACIÓN FUERA DE BANDA",
        "Queda estrictamente prohibido procesar cualquier solicitud de cambio de cuenta",
        "CLABE bancaria de proveedores de insumos dentales o remisión de expedientes",
        "recibida por correo sin completar el ciclo de verificación fuera de banda (OOB).",
        "",
        "CICLO OOB OBLIGATORIO:",
        "1. Detección de petición crítica (solicitud de fondos, datos o cuentas).",
        "2. Pausa inmediata de la transacción en recepción o consultorio.",
        "3. Llamada telefónica por segundo canal al número certificado en archivo físico.",
        "4. Confirmación verbal mediante clave preestablecida.",
        "5. Registro en bitácora administrativa de incidentes.",
    ],
    highlights=[3, 4, 5, 8, 9, 10]
)

create_code_screenshot(
    "figura_9_0_backup_script.png",
    "scripts/backup_db.sh",
    [
        "#!/usr/bin/env bash",
        "# scripts/backup_db.sh - Endurecimiento de permisos y respaldo cifrado AES-256",
        "umask 077",
        "chmod 600 ${DB_FILE} # Endurecimiento en disco contra lectura no autorizada",
        "",
        "# Respaldo consistente en caliente vía API SQLite",
        "sqlite3 \"${DB_FILE}\" \".backup '${BACKUP_RAW}'\"",
        "tar -czf \"${BACKUP_TAR}\" -C \"${BACKUP_DIR}\" \"$(basename ${BACKUP_RAW})\"",
        "",
        "# Cifrado militar simétrico GPG con algoritmo AES-256",
        "echo \"${PASSPHRASE}\" | gpg --batch --yes --passphrase-fd 0 \\",
        "    --symmetric --cipher-algo AES256 --output \"${BACKUP_ENC}\" \"${BACKUP_TAR}\"",
        "",
        "# Rotación automatizada de 30 días",
        "find \"${BACKUP_DIR}\" -name \"dentalsecurelab_*.tar.gz.gpg\" -mtime +30 -delete",
    ],
    highlights=[4, 7, 11, 14]
)

create_code_screenshot(
    "figura_10_0_network_hardening.png",
    "docs/network_hardening.md",
    [
        "# POLÍTICA DE ENDURECIMIENTO DE INFRAESTRUCTURA DE RED Y RACK (POL-NET-02)",
        "1. PROTECCIÓN FÍSICA EN RACK:",
        "   - Gabinete de acero laminado fijado rígidamente a muro con cerradura física.",
        "   - Llaves bajo custodia exclusiva de Administrador TI y Dirección Médica.",
        "",
        "2. SEGMENTACIÓN LÓGICA POR VLAN (IEEE 802.1Q):",
        "   - VLAN 10 (Médica y Administrativa): 192.168.10.0/24 (Consultorios 1-4, Servidor).",
        "   - VLAN 20 (Invitados y Pacientes): 192.168.20.0/24 (WiFi Sala de espera aislada).",
        "   - Regla de Firewall: Bloqueo total de comunicación entre VLAN 20 y VLAN 10.",
        "   - Directiva Client Isolation activada en el Punto de Acceso (WAP).",
    ],
    highlights=[3, 7, 8, 9]
)

# --- 10 GITHUB COMMIT SCREENSHOTS ---
create_github_commit_screenshot(
    "figura_1_1_github_commit_audit.png",
    "security/01-auditlog-traceability",
    "5c9d9db",
    "feat(audit): integrate django-auditlog and register clinical record models",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+55 -48 en 3 archivos (config/settings.py, records/models.py, requirements.txt)",
    [
        "@@ config/settings.py: INSTALLED_APPS & MIDDLEWARE @@",
        "+    'auditlog',",
        "+    'auditlog.middleware.AuditlogMiddleware',",
        "@@ records/models.py: registro de MedicalRecord @@",
        "+from auditlog.registry import auditlog",
        "+auditlog.register(MedicalRecord)",
        "@@ requirements.txt: dependencia de auditoría @@",
        "+django-auditlog>=3.0.0",
    ]
)

create_github_commit_screenshot(
    "figura_2_1_github_commit_idor.png",
    "security/02-idor-uuid-protection",
    "305fb8b",
    "fix(records): enforce object ownership and role check on record detail views",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+172 -18 en 9 archivos (records/, users/, templates/)",
    [
        "@@ records/models.py: campo UUID seguro @@",
        "+    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)",
        "@@ records/views.py: validación de rol y UUID lookup @@",
        "+    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'doctor']):",
        "+        raise PermissionDenied('Acceso denegado a expediente.')",
        "+    record = get_object_or_404(MedicalRecord, uuid=uuid)",
        "@@ templates/records/record_list.html: enlaces UUID @@",
        "-    <a href=\"{% url 'record_detail' record.pk %}\">",
        "+    <a href=\"{% url 'record_detail' record.uuid %}\">",
    ]
)

create_github_commit_screenshot(
    "figura_3_1_github_commit_ratelimit.png",
    "security/03-ratelimit-login",
    "d6a0680",
    "feat(auth): enforce ip rate limiting on login endpoint",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+135 -5 en 7 archivos (users/views.py, templates/users/login.html, ...)",
    [
        "@@ users/views.py: decorador ratelimit @@",
        "+@ratelimit(key='ip', rate='5/m', method='POST', block=False)",
        "+def login_view(request):",
        "+    if getattr(request, 'limited', False):",
        "+        return render(request, 'users/login.html', status=429)",
        "@@ config/urls.py: ruta login integrada @@",
        "+    path('login/', users_views.login_view, name='login'),",
    ]
)

create_github_commit_screenshot(
    "figura_4_1_github_commit_csrf.png",
    "security/04-csrf-hardening",
    "234dbfa",
    "fix(security): enforce CSRF cookie security flags and verify form tokens",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+5 -0 en 1 archivo (config/settings.py)",
    [
        "@@ config/settings.py: banderas de cookies CSRF @@",
        "+# CSRF Hardening (A-08 / A-48)",
        "+CSRF_COOKIE_HTTPONLY = True",
        "+CSRF_COOKIE_SECURE = True",
        "+CSRF_COOKIE_SAMESITE = 'Lax'",
    ]
)

create_github_commit_screenshot(
    "figura_5_1_github_commit_wal.png",
    "security/05-sqlite-wal-mode",
    "f340b1c",
    "perf(db): enable sqlite WAL mode and set busy timeout for concurrency",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+20 -0 en 2 archivos (core/apps.py, config/settings.py)",
    [
        "@@ core/apps.py: inyección de PRAGMAs vía conexión @@",
        "+def configure_sqlite_pragmas(sender, connection, **kwargs):",
        "+    if connection.vendor == 'sqlite':",
        "+        cursor.execute('PRAGMA journal_mode=WAL;')",
        "+        cursor.execute('PRAGMA busy_timeout=5000;')",
        "+        cursor.execute('PRAGMA synchronous=NORMAL;')",
    ]
)

create_github_commit_screenshot(
    "figura_6_1_github_commit_decouple.png",
    "security/06-env-secret-decouple",
    "f619c0c",
    "refactor(config): decouple settings and protect secret keys via environment variables",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+28 -3 en 4 archivos (.env.example, .gitignore, config/settings.py)",
    [
        "@@ config/settings.py: lectura con python-decouple @@",
        "-SECRET_KEY = 'django-insecure-...'",
        "+SECRET_KEY = config('SECRET_KEY', default='...')",
        "-DEBUG = True",
        "+DEBUG = config('DEBUG', default=False, cast=bool)",
        "@@ .gitignore: exclusión estricta @@",
        "+!.env.example",
    ]
)

create_github_commit_screenshot(
    "figura_7_1_github_commit_nginx.png",
    "security/07-https-hsts-headers",
    "2b92de7",
    "infra(nginx): define SSL reverse proxy configuration and HSTS headers",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+96 -0 en 2 archivos (deploy/nginx/dentalsecurelab.conf, config/settings.py)",
    [
        "@@ deploy/nginx/dentalsecurelab.conf: TLS y cabeceras @@",
        "+server { listen 80; return 301 https://$host$request_uri; }",
        "+server { listen 443 ssl http2;",
        "+    add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains' always;",
        "+    proxy_pass http://127.0.0.1:8000; }",
    ]
)

create_github_commit_screenshot(
    "figura_8_1_github_commit_antiphishing.png",
    "security/08-antiphishing-procedure",
    "b2facfb",
    "docs(security): establish anti-phishing SOP and out-of-band verification protocol",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+101 -0 en 1 archivo (docs/sop_antiphishing.md)",
    [
        "@@ docs/sop_antiphishing.md: creación de SOP-SEC-01 @@",
        "+# PROCEDIMIENTO OPERATIVO ESTÁNDAR (SOP-SEC-01)",
        "+# PROTOCOLO DE PREVENCIÓN DE INGENIERÍA SOCIAL Y VERIFICACIÓN FUERA DE BANDA",
        "+Queda estrictamente prohibido procesar transferencias o modificaciones",
        "+sin verificación previa vía canal telefónico secundario certificado.",
    ]
)

create_github_commit_screenshot(
    "figura_9_1_github_commit_backup.png",
    "security/09-filesystem-db-protection",
    "c8aab27",
    "chore(scripts): create automated backup and filesystem permission hardening script",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+78 -0 en 1 archivo (scripts/backup_db.sh)",
    [
        "@@ scripts/backup_db.sh: respaldo seguro y cifrado @@",
        "+chmod 600 \"${DB_FILE}\"",
        "+sqlite3 \"${DB_FILE}\" \".backup '${BACKUP_RAW}'\"",
        "+gpg --batch --symmetric --cipher-algo AES256 --output \"${BACKUP_ENC}\"",
        "+sha256sum \"${BACKUP_ENC}\" >> \"${LOG_FILE}\"",
    ]
)

create_github_commit_screenshot(
    "figura_10_1_github_commit_network.png",
    "security/10-network-rack-hardening",
    "217c97e",
    "docs(network): document VLAN segmentation and router hardening baseline",
    "Aldo Pérez <perezaldo435@gmail.com>",
    "16 Sep 2026",
    "+79 -0 en 1 archivo (docs/network_hardening.md)",
    [
        "@@ docs/network_hardening.md: política de red y rack @@",
        "+# POLÍTICA DE ENDURECIMIENTO DE INFRAESTRUCTURA DE RED Y RACK",
        "+- Rack cerrado bajo llave de acero laminado para conmutadores y servidor.",
        "+- Segmentación lógica IEEE 802.1Q: VLAN 10 (Médica) vs VLAN 20 (Pacientes).",
        "+- Bloqueo absoluto de administración WAN en enrutador perimetral.",
    ]
)

# --- 4 USER SCREENSHOTS ---
def render_login_ui(draw, x, y, w, h):
    # Centered card
    cx = x + (w - 400) // 2
    cy = y + 20
    draw.rounded_rectangle([(cx, cy), (cx + 400, cy + 340)], radius=8, fill=(255, 255, 255), outline=(226, 232, 240))
    
    draw.text((cx + 100, cy + 25), "Acceso al Sistema Clínico", font=FONT_UI_BOLD, fill=(30, 41, 59))
    draw.text((cx + 115, cy + 50), "Autenticación Segura DentalSecureLab", font=FONT_SMALL, fill=(100, 116, 139))
    
    # Rate limit banner
    draw.rounded_rectangle([(cx + 25, cy + 78), (cx + 375, cy + 115)], radius=6, fill=(254, 242, 242), outline=(239, 68, 68))
    draw.text((cx + 35, cy + 85), "⚠️ Límite activo: Máximo 5 intentos/min por IP", font=FONT_SMALL, fill=(153, 27, 27))
    draw.text((cx + 35, cy + 98), "Protección contra fuerza bruta y diccionario", font=FONT_SMALL, fill=(185, 28, 28))
    
    # Inputs
    draw.text((cx + 25, cy + 130), "Usuario Institucional", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(cx + 25, cy + 150), (cx + 375, cy + 185)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((cx + 35, cy + 158), "dr_odontologo1", font=FONT_UI, fill=(30, 41, 59))
    
    draw.text((cx + 25, cy + 200), "Contraseña", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(cx + 25, cy + 220), (cx + 375, cy + 255)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((cx + 35, cy + 228), "••••••••••••••••", font=FONT_UI, fill=(30, 41, 59))
    
    # Button
    draw.rounded_rectangle([(cx + 25, cy + 275), (cx + 375, cy + 315)], radius=6, fill=(2, 132, 199))
    draw.text((cx + 140, cy + 287), "Ingresar al Sistema", font=FONT_UI_BOLD, fill=(255, 255, 255))

create_ui_screenshot(
    "figura_11_usuario_login.png",
    "Inicio de Sesión y Control de Autenticación",
    "Acceso individual con protección activa de limitación de tasa por dirección IP (HTTP 429)",
    render_login_ui
)

def render_bloqueo_ui(draw, x, y, w, h):
    # Dark overlay simulating screen lock
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=8, fill=(15, 23, 42))
    
    cx = x + (w - 440) // 2
    cy = y + 50
    draw.rounded_rectangle([(cx, cy), (cx + 440, cy + 260)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105))
    
    draw.text((cx + 185, cy + 25), "🔒", font=FONT_TITLE, fill=(255, 255, 255))
    draw.text((cx + 90, cy + 60), "Sesión Bloqueada por Inactividad", font=FONT_UI_BOLD, fill=(255, 255, 255))
    draw.text((cx + 70, cy + 90), "Han transcurrido 5 minutos sin actividad en el consultorio.", font=FONT_SMALL, fill=(148, 163, 184))
    draw.text((cx + 95, cy + 110), "Ingrese su contraseña para reanudar el expediente.", font=FONT_SMALL, fill=(148, 163, 184))
    
    draw.rounded_rectangle([(cx + 40, cy + 145), (cx + 400, cy + 185)], radius=6, fill=(15, 23, 42), outline=(71, 85, 105))
    draw.text((cx + 55, cy + 155), "••••••••••••••••", font=FONT_UI, fill=(226, 232, 240))
    
    draw.rounded_rectangle([(cx + 40, cy + 200), (cx + 400, cy + 240)], radius=6, fill=(14, 165, 233))
    draw.text((cx + 160, cy + 212), "Desbloquear Estación", font=FONT_UI_BOLD, fill=(255, 255, 255))

create_ui_screenshot(
    "figura_12_usuario_bloqueo.png",
    "Seguridad en Consultorio: Bloqueo Automático tras 5 Minutos",
    "Protección activa del expediente del paciente ante abandono físico temporal del consultorio",
    render_bloqueo_ui
)

def render_pagos_ui(draw, x, y, w, h):
    # Payment form card
    draw.rounded_rectangle([(x + 20, y + 10), (x + w - 20, y + h - 10)], radius=8, fill=(255, 255, 255), outline=(226, 232, 240))
    
    draw.text((x + 40, y + 25), "Registrar Pago de Tratamiento Odontológico", font=FONT_UI_BOLD, fill=(30, 41, 59))
    draw.text((x + 40, y + 50), "Operación de caja protegida con token CSRF y cookie HttpOnly", font=FONT_SMALL, fill=(100, 116, 139))
    
    # CSRF Badge
    draw.rounded_rectangle([(x + w - 220, y + 25), (x + w - 40, y + 55)], radius=4, fill=(240, 253, 244), outline=(74, 222, 128))
    draw.text((x + w - 210, y + 32), "🛡️ CSRF Token Verified", font=FONT_BADGE, fill=(22, 101, 52))
    
    draw.line([(x + 40, y + 75), (x + w - 40, y + 75)], fill=(241, 245, 249), width=1)
    
    # Fields
    draw.text((x + 40, y + 90), "Paciente:", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(x + 40, y + 110), (x + 380, y + 145)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((x + 50, y + 120), "Carlos Mendoza Silva", font=FONT_UI, fill=(30, 41, 59))
    
    draw.text((x + 400, y + 90), "Fecha:", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(x + 400, y + 110), (x + w - 40, y + 145)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((x + 410, y + 120), "16/09/2026", font=FONT_UI, fill=(30, 41, 59))
    
    draw.text((x + 40, y + 160), "Concepto de Atención:", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(x + 40, y + 180), (x + 380, y + 215)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((x + 50, y + 190), "Endodoncia pieza 24 + Resina", font=FONT_UI, fill=(30, 41, 59))
    
    draw.text((x + 400, y + 160), "Monto a Cobrar ($ MXN):", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(x + 400, y + 180), (x + w - 40, y + 215)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((x + 410, y + 190), "$ 2,850.00", font=FONT_UI_BOLD, fill=(16, 185, 129))
    
    draw.text((x + 40, y + 230), "Método de Pago:", font=FONT_BADGE, fill=(71, 85, 105))
    draw.rounded_rectangle([(x + 40, y + 250), (x + 380, y + 285)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((x + 50, y + 260), "Transferencia SPEI (Validada OOB)", font=FONT_UI, fill=(30, 41, 59))
    
    draw.rounded_rectangle([(x + 40, y + 310), (x + 220, y + 350)], radius=6, fill=(2, 132, 199))
    draw.text((x + 75, y + 322), "Guardar Pago", font=FONT_UI_BOLD, fill=(255, 255, 255))

create_ui_screenshot(
    "figura_13_usuario_pagos.png",
    "Módulo de Caja y Captura de Pagos en Recepción",
    "Formulario transaccional con token CSRF y validación de cobro",
    render_pagos_ui
)

def render_incidentes_ui(draw, x, y, w, h):
    draw.rounded_rectangle([(x + 20, y + 10), (x + w - 20, y + h - 10)], radius=8, fill=(255, 255, 255), outline=(226, 232, 240))
    
    draw.text((x + 40, y + 25), "Protocolo de Notificación de Incidentes de Ciberseguridad", font=FONT_UI_BOLD, fill=(153, 27, 27))
    draw.text((x + 40, y + 50), "Canal de escalamiento rápido e instrucciones inmediatas ante sospecha de compromiso", font=FONT_SMALL, fill=(100, 116, 139))
    
    draw.line([(x + 40, y + 75), (x + w - 40, y + 75)], fill=(241, 245, 249), width=1)
    
    steps = [
        ("PASO 1: Desconexión Física Inmediata", "Desconecte el cable Ethernet RJ-45 de la parte trasera del equipo."),
        ("PASO 2: No apague el equipo", "Mantenga la pantalla encendida para preservar evidencias volátiles en RAM."),
        ("PASO 3: Notificación Inmediata a TI", "Contacte al Administrador TI mediante la extensión interna 101 en menos de 10 min."),
        ("PASO 4: Registro de Formato Físico", "Complete el formulario de reporte de incidente consignando consultorio y hora.")
    ]
    
    sy = y + 90
    for title, desc in steps:
        draw.rounded_rectangle([(x + 40, sy), (x + w - 40, sy + 50)], radius=6, fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((x + 55, sy + 8), title, font=FONT_BADGE, fill=(30, 41, 59))
        draw.text((x + 55, sy + 28), desc, font=FONT_SMALL, fill=(71, 85, 105))
        sy += 60

create_ui_screenshot(
    "figura_14_usuario_reporte_incidentes.png",
    "Canal de Respuesta Rápida y Notificación de Incidentes",
    "Guía visual paso a paso para doctores y recepcionista ante anomalías",
    render_incidentes_ui
)

print("All 24 screenshots generated successfully in docs/screenshots/!")
