# 🦷🔐 DentalSecureLab

**DentalSecureLab** es una aplicación web educativa desarrollada con **Python y Django** para utilizarse como entorno práctico en el aprendizaje de **seguridad en entornos digitales**.

El proyecto simula un sistema básico de gestión para un consultorio dental y proporciona una infraestructura controlada sobre la cual los estudiantes pueden implementar, configurar y evaluar diferentes mecanismos de seguridad.

> ⚠️ Este proyecto tiene fines exclusivamente educativos.  
> No debe utilizarse para almacenar información clínica, financiera o personal real.

---

## 🎯 Objetivo del proyecto

DentalSecureLab busca proporcionar una aplicación web funcional sobre la cual los estudiantes puedan desarrollar prácticas relacionadas con:

- Configuración de servidores Linux.
- Protección de comunicaciones.
- Implementación de controles de seguridad.
- Hardening de servidores.
- Autenticación y control de acceso.
- Análisis de vulnerabilidades.
- Seguridad de aplicaciones web.
- Pentesting en un entorno controlado.

La aplicación funciona como un **laboratorio progresivo**, por lo que su seguridad será fortalecida conforme avancen las prácticas.

---

## 🏗️ Arquitectura Integral del Sistema y Laboratorio

El proyecto está diseñado bajo un enfoque dual: un **laboratorio formativo para equipos de dos estudiantes** (defensa vs evaluación) y una **arquitectura de producción con Defensa en Profundidad (Defense-in-Depth)** orientada a la protección de datos clínicos sensibles.

---

### 1. Entorno de Laboratorio Educativo (Parejas)

El laboratorio organiza el trabajo en dos perfiles complementarios:

```text
        ESTUDIANTE A                         ESTUDIANTE B
           Laptop                               Laptop
             │                                    │
      Máquina Virtual                      Máquina Virtual
             │                                    │
      Ubuntu Server                          Kali Linux
             │                                    │
      DentalSecureLab                       OWASP ZAP
             │                              Pentesting
      Django + SQLite                            │
             │                                    │
             └────────── RED LOCAL ───────────────┘
                       Router / Switch
```

* **Estudiante A (Defensivo / SysAdmin / Developer):** Despliega, endurece y administra DentalSecureLab sobre **Ubuntu Server**, configurando Nginx, cortafuegos, certificados TLS y políticas de acceso.
* **Estudiante B (Ofensivo / Auditor de Seguridad):** Utiliza **Kali Linux**, OWASP ZAP y herramientas de análisis para evaluar y verificar los controles de seguridad implementados dentro de un entorno controlado y autorizado.

---

### 2. Diagrama de Arquitectura de Extremo a Extremo

El siguiente diagrama modela el flujo completo de la plataforma: estaciones de trabajo clínicas en consultorios, red segmentada, entorno de auditoría, reverse proxy perimetral, middleware de seguridad, aplicaciones de dominio Django, persistencia en SQLite (WAL) y gobernanza técnica:

```mermaid
flowchart TB

    %% Usuarios y entorno clínico
    subgraph users["1. Clientes y Entorno de Acceso (VLAN 10 Médica)"]
        c1["Consultorio 1<br/>Dr. General"]
        c2["Consultorio 2<br/>Dr. General"]
        c3["Consultorio 3<br/>Dra. General"]
        c4["Consultorio 4<br/>Especialistas"]
        nurse["Asistente Dental /<br/>Enfermero"]
        recep["Recepción / Caja<br/>Atención a Pacientes"]
        admin_user["Administrador TI /<br/>Superusuario"]
    end

    %% Entorno de evaluación de seguridad
    subgraph assessment["Entorno de Auditoría y Evaluación"]
        kali["Kali Linux Auditor"]
        zap["OWASP ZAP /<br/>Escáner de Seguridad"]
        audit_tools["Herramientas de Pentesting<br/>Autorizadas"]
    end

    %% Infraestructura perimetral y servidor
    subgraph infrastructure["2. Infraestructura y Despliegue (Rack Cerrado)"]
        network["Switch Administrado<br/>VLAN 10 (Médica) vs VLAN 20 (Pacientes)"]
        firewall["Firewall Perimetral<br/>iptables / DROP by Default"]
        nginx["Nginx 1.24<br/>Reverse Proxy + Terminación TLS 1.3<br/>HSTS 31536000 + Security Headers"]
        gunicorn["Gunicorn WSGI Application Cluster<br/>Workers Síncronos en Localhost:8000"]
        env["Entorno Virtual Python (.venv)"]
        config["Configuración Desacoplada<br/>config/settings.py + python-decouple"]
        env_file[".env / .env.example<br/>Variables de Entorno Sanitizadas"]
    end

    %% Aplicación Django
    subgraph django["3. Capa de Aplicación Django 6.1"]
        manage["manage.py<br/>CLI de Gestión"]

        subgraph middleware["Cadena de Middlewares de Seguridad"]
            sec_mw["SecurityMiddleware (HSTS/SSL)"]
            sess_mw["SessionMiddleware (HttpOnly/Secure)"]
            csrf_mw["CsrfViewMiddleware (Token Hash)"]
            auth_mw["AuthenticationMiddleware"]
            audit_mw["AuditlogMiddleware (Trazabilidad IP/User)"]
        end

        subgraph routing["Enrutamiento y Presentación"]
            urls["config/urls.py<br/>Dispatcher de Rutas"]
            templates["templates/<br/>HTML Seguro (Jinja)"]
            static["static/<br/>CSS, Iconos y Assets"]
            dashboard["Dashboard Clínico<br/>Resumen General"]
        end

        subgraph modules["Módulos Funcionales (Dominio Clínico)"]
            users_app["users<br/>Autenticación, RBAC y<br/>LoginAttemptTracker (Fuerza Bruta)"]
            patients["patients<br/>Padrón de Pacientes"]
            agenda["agenda<br/>Citas y Turnos"]
            records["records<br/>Expedientes Clínicos<br/>Lookup por UUID v4 (Anti-IDOR)"]
            payments["payments<br/>Caja y Transacciones<br/>Protección CSRF Obligatoria"]
            core["core<br/>Agregación Métrica y Señales WAL"]
        end
    end

    %% Datos y Persistencia
    subgraph data["4. Persistencia y Almacenamiento Cifrado"]
        sqlite[("SQLite 3 (db.sqlite3)<br/>journal_mode = WAL<br/>busy_timeout = 5000ms<br/>Permisos chmod 600")]
        wal_files["Archivos Temporales WAL<br/>db.sqlite3-wal / db.sqlite3-shm"]
        migrations["Migraciones Versionadas<br/>(users, records, auditlog)"]
        backup["scripts/backup_db.sh<br/>Respaldo en Caliente + Cifrado GPG AES-256"]
    end

    %% Gobernanza y Documentación
    subgraph operations["5. Gobernanza, Operación y Seguridad"]
        docs["docs/<br/>Manuales y Reportes Técnicos"]
        sop["SOP_ANTIPHISHING<br/>Verificación Fuera de Banda"]
        net_doc["NETWORK_HARDENING<br/>Línea Base Rack y VLANs"]
        sec_mat["POLITICAS_Y_MATRICES<br/>POL-SEC-ACC-01 y RBAC"]
        requirements["requirements.txt<br/>Dependencias Fijas"]
    end

    %% Flujos de Clientes Clínicos
    c1 & c2 & c3 & c4 & nurse & recep & admin_user --> network
    network --> firewall
    firewall -->|"HTTPS / Puerto 443"| nginx
    nginx -->|"Proxy HTTP Local / 127.0.0.1:8000"| gunicorn
    gunicorn --> sec_mw
    sec_mw --> sess_mw --> csrf_mw --> auth_mw --> audit_mw --> urls

    %% Flujo de Auditoría
    kali --> zap --> audit_tools
    audit_tools -.->|"Evaluación Controlada"| nginx

    %% Despacho de Rutas
    urls --> users_app
    urls --> dashboard
    urls --> patients
    urls --> agenda
    urls --> records
    urls --> payments

    %% Presentación
    dashboard & users_app & patients & agenda & records & payments --> templates
    templates --> static

    %% Dependencias Core
    core --> dashboard
    dashboard -.->|"Métricas"| patients
    dashboard -.->|"Métricas"| agenda
    dashboard -.->|"Métricas"| records
    dashboard -.->|"Métricas"| payments

    %% Relaciones entre Módulos
    agenda -->|"Citas asociadas"| patients
    records -->|"Expediente único (UUID)"| patients
    payments -->|"Pagos de tratamientos"| patients
    users_app -->|"Control RBAC estricto"| records
    users_app -->|"Restricción de caja"| payments

    %% Persistencia hacia la Base de Datos
    users_app & patients & agenda & records & payments --> sqlite
    sqlite --- wal_files
    manage --> migrations --> sqlite
    manage --> config --> env_file
    backup -->|"Copia consistente .backup"| sqlite

    %% Estilos Visuales
    classDef userCls fill:#e0f2fe,stroke:#0284c7,stroke-width:1.5px,color:#0c4a6e
    classDef infraCls fill:#ede9fe,stroke:#7c3aed,stroke-width:1.5px,color:#4c1d95
    classDef appCls fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
    classDef dataCls fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
    classDef secCls fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337

    class c1,c2,c3,c4,nurse,recep,admin_user userCls
    class kali,zap,audit_tools secCls
    class network,firewall,nginx,gunicorn,env,config,env_file infraCls
    class manage,sec_mw,sess_mw,csrf_mw,auth_mw,audit_mw,urls,templates,static,dashboard,users_app,patients,agenda,records,payments,core appCls
    class sqlite,wal_files,migrations,backup dataCls
    class docs,sop,net_doc,sec_mat,requirements secCls

    %% Enlaces a código fuente
    click manage "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/manage.py"
    click config "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/config/settings.py"
    click urls "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/config/urls.py"
    click dashboard "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/core/views.py"
    click users_app "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/users/models.py"
    click patients "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/patients/models.py"
    click agenda "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/agenda/models.py"
    click records "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/records/models.py"
    click payments "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/payments/models.py"
    click nginx "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/deploy/nginx/dentalsecurelab.conf"
    click backup "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/scripts/backup_db.sh"
    click docs "https://github.com/Ing-Aldo-coder/DentalSecureLab/blob/main/docs/arquitectura.md"
```

---

### 3. Capas de Defensa en Profundidad

| Capa | Componente | Mecanismos y Controles de Seguridad |
| :--- | :--- | :--- |
| **Capa 1: Clientes y Terminales** | 4 Consultorios + Recepción | Bloqueo por inactividad tras **5 minutos**, autenticación personal no compartida, segmento exclusivo **VLAN 10 Médica** (`192.168.10.0/24`). |
| **Capa 2: Perímetro y Transporte** | Nginx 1.24 Reverse Proxy | **TLS v1.3**, redirección 301 forzada HTTP->HTTPS, cabeceras HSTS (`max-age=31536000`), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`. Bloqueo directo de accesos a `.sqlite3`, `.sh`, `.env`. |
| **Capa 3: Servidor WSGI** | Gunicorn Cluster | Workers síncronos sobre `.venv`, enlace exclusivo a `127.0.0.1:8000` (sin exposición externa). |
| **Capa 4: Aplicación Web** | Django 6.1 Framework | Middlewares en cascada (`Security`, `Session`, `CSRF`, `Authentication`, `Auditlog`), RBAC estricto, mitigación IDOR por **UUID v4**, bloqueo progresivo de intentos fallidos de login (`LoginAttemptTracker`), gestión de variables desacopladas vía `python-decouple`. |
| **Capa 5: Persistencia de Datos** | SQLite 3 (Modo WAL) | `PRAGMA journal_mode=WAL;` y `PRAGMA busy_timeout=5000;` para concurrencia multi-consultorio sin contención, permisos `chmod 600`, respaldos consistentes en caliente con cifrado simétrico **GPG AES-256** (`backup_db.sh`). |

---

### 4. Modelo Relacional de Base de Datos

```mermaid
erDiagram
    USERS_USER ||--o| USERS_USERPROFILE : "posee perfil y rol RBAC"
    USERS_USER ||--o{ USERS_LOGINATTEMPTTRACKER : "monitoreo por IP"
    PATIENTS_PATIENT ||--o| RECORDS_MEDICALRECORD : "expediente clínico único"
    PATIENTS_PATIENT ||--o{ AGENDA_APPOINTMENT : "registra citas"
    PATIENTS_PATIENT ||--o{ PAYMENTS_PAYMENT : "efectúa pagos"

    USERS_USER {
        int id PK
        string username UK
        string password_hash "PBKDF2 SHA-256"
        boolean is_superuser
    }

    USERS_USERPROFILE {
        int id PK
        int user_id FK
        string role "admin, doctor, nurse, receptionist"
    }

    USERS_LOGINATTEMPTTRACKER {
        int id PK
        string ip_address UK
        int failed_attempts
        datetime blocked_until
        int stage "0: Normal, 1: 5min, 2: 30min"
        int post_block_attempts
    }

    PATIENTS_PATIENT {
        int id PK
        string first_name
        string last_name
        date birth_date
        string phone
        string email
        text address
        datetime created_at
    }

    RECORDS_MEDICALRECORD {
        int id PK
        uuid uuid UK "UUID v4 Criptográfico (Anti-IDOR)"
        int patient_id FK,UK "Relación 1 a 1"
        text reason "Motivo de consulta"
        text diagnosis "Diagnóstico clínico confidencial"
        text treatment "Tratamiento odontológico"
        text observations "Notas clínicas"
        datetime created_at
        datetime updated_at
    }

    AGENDA_APPOINTMENT {
        int id PK
        int patient_id FK
        date date
        time time
        string reason
        string status "scheduled, confirmed, completed, cancelled"
        text notes
    }

    PAYMENTS_PAYMENT {
        int id PK
        int patient_id FK
        date date
        string concept
        decimal amount "Monto numérico"
        string payment_method "cash, card, transfer"
        text notes
    }
```

---

### 5. Ciclo de Vida de una Petición HTTP Segura

```text
[Terminal en Consultorio] (Navegador Web)
           │
           │  1. Petición HTTPS (TLS v1.3)
           ▼
[Nginx Reverse Proxy]
           │  2. Validación TLS, cabeceras HSTS y redirección 301
           │  3. Proxy hacia 127.0.0.1:8000 con cabecera X-Forwarded-Proto
           ▼
[Gunicorn WSGI Server]
           │  4. Despacho a Worker activo en entorno .venv
           ▼
[Pipeline de Middlewares Django]
           │  5. SecurityMiddleware: Fuerza canal seguro
           │  6. SessionMiddleware: Valida cookies HttpOnly, Secure, SameSite=Lax
           │  7. CsrfViewMiddleware: Comprobación estricta de token anti-CSRF
           │  8. AuthenticationMiddleware: Carga identidad en request.user
           │  9. AuditlogMiddleware: Registro transaccional de IP, usuario y mutación
           ▼
[Vista / Controlador RBAC] (e.g. record_detail)
           │  10. Validación de rol (@login_required, permisos doctor/admin)
           │  11. Consulta de expediente por UUID v4 (Prevención de IDOR)
           ▼
[Django ORM & SQLite WAL]
           │  12. PRAGMA journal_mode=WAL permite lectura paralela sin bloqueo
           ▼
[Renderizado de Plantilla HTML]
           │  13. Escape contextual automático contra XSS
           ▼
[Respuesta HTTP 200]
           │  14. Entrega cifrada a la estación del consultorio
```

---

### 6. Segmentación de Red y Topología Física (IEEE 802.1Q)

```text
                      INTERNET
                         │
                         ▼
             [Router / Puerta de Enlace]
               (Bloqueo de Gestión WAN)
                         │
                         ▼
        [Switch Central Administrado IEEE 802.1Q]
         (Ubicado en Gabinete Rack con Llave)
            ├── Trunk
            │
    ┌───────┴────────────────────────┐
    ▼                                ▼
[VLAN 10: Médica y Operativa]   [VLAN 20: Pacientes e Invitados]
Segmento: 192.168.10.0/24       Segmento: 192.168.20.0/24
Asignación: Reserva MAC fija    Asignación: DHCP Dinámico
- Consultorios 1, 2, 3 y 4      - Wi-Fi en Sala de Espera
- Terminal de Recepción         - Client Isolation Activo
- Servidor DentalSecureLab      - Cero visibilidad a VLAN 10
```

> 📘 **Documento Técnico Completo:** Para profundizar en especificaciones de hardening, reglas de configuración y guías operativas, consulte [docs/arquitectura.md](docs/arquitectura.md).

---

## 💻 Tecnologías

### Aplicación

- Python
- Django
- HTML
- CSS
- SQLite

### Infraestructura y seguridad

A lo largo del laboratorio podrán incorporarse tecnologías como:

- Ubuntu Server
- Linux
- Git
- Nginx / Apache
- OpenSSL
- Firewall
- Kali Linux
- OWASP ZAP

---

## 📦 Funcionalidades actuales

DentalSecureLab incluye los siguientes módulos:

### 👤 Pacientes

Permite registrar y consultar pacientes dentro del sistema.

### 📅 Agenda

Permite registrar y administrar citas asociadas con los pacientes.

### 📋 Expedientes

Permite crear expedientes clínicos asociados con los pacientes.

### 💳 Pagos

Permite registrar los pagos realizados y consultar los movimientos almacenados.

### 📊 Dashboard

Presenta información general de los registros existentes en el sistema.

---

# 🚀 Instalación del laboratorio

## 1. Actualizar Ubuntu Server

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 2. Instalar Git y Python

```bash
sudo apt install git python3 python3-pip python3-venv -y
```

Comprobar las instalaciones:

```bash
git --version
python3 --version
```

---

## 3. Clonar DentalSecureLab

```bash
git clone https://github.com/atonaltzin/DentalSecureLab.git
```

Entrar al proyecto:

```bash
cd DentalSecureLab
```

---

## 4. Crear el entorno virtual

```bash
python3 -m venv env
```

Activarlo:

```bash
source env/bin/activate
```

Cuando el entorno esté activo deberá aparecer:

```text
(env)
```

al inicio de la terminal.

---

## 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 6. Crear la base de datos

La base de datos **no se distribuye dentro del repositorio**.

Cada instalación deberá generar su propia base de datos mediante las migraciones de Django:

```bash
python manage.py migrate
```

Esto generará localmente:

```text
db.sqlite3
```

---

## 7. Crear usuario administrador

```bash
python manage.py createsuperuser
```

Django solicitará los datos necesarios para crear la cuenta administrativa.

---

## 8. Ejecutar DentalSecureLab

Para comprobar inicialmente la instalación:

```bash
python manage.py runserver
```

La aplicación estará disponible localmente en:

```text
http://127.0.0.1:8000
```

> La configuración para permitir el acceso desde otros equipos de la red forma parte de las prácticas del laboratorio y no se encuentra preconfigurada.

---

# 🧪 Preparación del laboratorio

Después de realizar la instalación, cada equipo deberá generar información **completamente ficticia** para trabajar durante las prácticas.

Como conjunto inicial se recomienda registrar:

| Información | Cantidad mínima |
|---|---:|
| Pacientes ficticios | 10 |
| Citas | 10 |
| Expedientes | 10 |
| Pagos | 10 |

**No utilizar datos personales, médicos o financieros reales.**

---

# 🔐 Ruta de aprendizaje

DentalSecureLab está diseñado para evolucionar progresivamente durante el curso.

```text
C1
Protección de comunicaciones
        ↓
C2
Requisitos y controles de seguridad
        ↓
C3
Protección del servidor
        ↓
C4
Usuarios y autenticación
        ↓
C5
Evaluación de seguridad
```

Cada etapa incorpora nuevos controles sobre la misma infraestructura, permitiendo observar la evolución de una aplicación web desde su configuración inicial hasta la evaluación de su seguridad.

---

# ⚠️ Consideraciones de seguridad

DentalSecureLab constituye un **entorno educativo de laboratorio**.

Algunas configuraciones pueden ser deliberadamente básicas o formar parte de ejercicios posteriores de análisis y fortalecimiento.

Las pruebas de seguridad deberán realizarse exclusivamente:

- Sobre infraestructura propia.
- Dentro del laboratorio autorizado.
- Entre los equipos designados para la práctica.
- Con información ficticia.
- Bajo las indicaciones del docente.

Nunca deben realizarse pruebas sobre sistemas, redes, aplicaciones o dispositivos sin autorización.

---

# 📁 Estructura general

```text
DentalSecureLab/
│
├── agenda/
├── config/
├── core/
├── patients/
├── payments/
├── records/
├── users/
│
├── static/
├── templates/
│
├── manage.py
├── requirements.txt
└── .gitignore
```

El entorno virtual y la base de datos se generan localmente y no forman parte del repositorio:

```text
env/
db.sqlite3
```

---

# 📚 Uso educativo

Este proyecto puede utilizarse como apoyo para cursos relacionados con:

- Seguridad en entornos digitales.
- Ciberseguridad.
- Seguridad web.
- Administración de servidores.
- Desarrollo seguro de aplicaciones.
- Fundamentos de pentesting.
- Ingeniería de software.

El proyecto continuará evolucionando conforme se desarrollen nuevas prácticas y materiales educativos.

---

## 👨‍💻 Autor

**José Atonaltzin Maldonado Ortiz**

Docente y profesional del área de Tecnologías de la Información.

Áreas de trabajo e interés:

- Ingeniería de Software
- Desarrollo Web
- Ciberseguridad
- Tecnologías de la Información
- Docencia tecnológica

---

## 🤝 Contribuciones

Las sugerencias, correcciones y mejoras al proyecto son bienvenidas.

Puedes utilizar las herramientas de GitHub para:

- Reportar errores.
- Proponer mejoras.
- Realizar un fork del proyecto.
- Enviar contribuciones mediante Pull Requests.

---

## 📄 Licencia

La licencia de distribución y reutilización del proyecto se encuentra pendiente de definición.

---

**DentalSecureLab**  
*Un laboratorio educativo para aprender seguridad construyendo, protegiendo y evaluando una aplicación web.*