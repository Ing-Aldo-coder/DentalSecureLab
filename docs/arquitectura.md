# ARQUITECTURA INTEGRAL DE LA APLICACIÓN Y SISTEMA CLÍNICO
## PLATAFORMA INTEGRAL DENTALSECURELAB
**Documento Técnico Oficial:** ARQ-SYS-2026-FINAL | **Versión:** 2.0  
**Fecha de Emisión:** 17 de Septiembre de 2026  
**Dirección Responsable:** Arquitectura de Software, Seguridad Informática y DevOps  
**Clasificación:** Confidencial - Uso Interno e Infraestructura  

---

## 1. VISIÓN GENERAL Y CONTEXTO OPERATIVO

DentalSecureLab es una plataforma web integral diseñada para la gestión clínica, administrativa y financiera de una clínica odontológica de alta demanda. La solución ha sido construida bajo el principio de **Defensa en Profundidad (Defense-in-Depth)**, garantizando que el tratamiento de datos médicos altamente sensibles (diagnósticos, antecedentes patológicos y tratamientos) y transacciones financieras se ejecuten en un entorno blindado, resiliente y de estricto cumplimiento normativo.

### Contexto Operativo y Talento Humano
El sistema opera sobre una infraestructura local distribuida que da soporte a:
* **4 Consultorios Odontológicos Especializados:** Equipados con terminales dedicadas para médicos generales y especialistas.
* **1 Central de Recepción Administrativa:** Terminal encargada de altas demográficas, agendamiento de citas y captura de cobros.
* **Plantilla Fija de 8 Colaboradores con Roles RBAC:**
  * 3 Odontólogos Generales (`doctor`).
  * 2 Especialistas Odontológicos (Endodoncia y Ortodoncia - `doctor`).
  * 1 Asistente Dental / Enfermero (`nurse` - lectura y captura asistida).
  * 1 Recepcionista (`receptionist` - caja, pacientes y citas; sin acceso a expedientes).
  * 1 Administrador de TI y Soporte (`admin` - superusuario, sin acceso a expedientes clínicos confidenciales).

---

## 2. DIAGRAMA DE ARQUITECTURA GENERAL DEL SISTEMA

El siguiente diagrama modela la arquitectura completa de extremo a extremo: clientes clínicos, entorno de evaluación, capas de infraestructura, enrutamiento, lógica de negocio Django, persistencia y gobernanza operativa.

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

    %% Estilos Visuales de Alto Contraste
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
```

---

## 3. ARQUITECTURA POR CAPAS (DEFENSA EN PROFUNDIDAD)

La aplicación implementa una separación estricta en **5 capas arquitectónicas**, donde cada nivel actúa como una barrera de contención independiente:

### Capa 1: Clientes y Entorno de Acceso (Terminales de Consultorio)
* **Hardware:** Estaciones de cómputo ubicadas en los 4 consultorios y recepción.
* **Seguridad de Estación:**
  * Bloqueo obligatorio por inactividad tras **5 minutos** (directiva de SO / `Windows + L`).
  * Autenticación individual intransferible; prohibición expresa de cuentas compartidas.
  * Acceso exclusivo a través del segmento `192.168.10.0/24` (**VLAN 10 Médica**).

### Capa 2: Infraestructura Perimetral y Transporte (Nginx Reverse Proxy)
* **Componente:** Servidor Nginx 1.24 alojado en Ubuntu Server dentro de un gabinete rack bajo llave.
* **Políticas de Transporte y Perímetro:**
  * **Terminación Criptográfica:** Exclusivamente **TLS v1.3** con suites de cifrado de secreto perfecto hacia adelante (PFS).
  * **Redirección Forzada:** HTTP (Puerto 80) redirigido permanentemente con código **301** hacia HTTPS (Puerto 443).
  * **Cabeceras de Seguridad Inyectadas:**
    * `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` (HSTS a 1 año).
    * `X-Frame-Options: DENY` (Mitigación total contra Clickjacking).
    * `X-Content-Type-Options: nosniff` (Mitigación de MIME-Sniffing).
  * **Aislamiento de Archivos Sensibles:** Regla de bloqueo directo en Nginx para cualquier intento de lectura a archivos con extensión `.sqlite3`, `.sh` o `.env`.

### Capa 3: Servidor de Aplicaciones WSGI (Gunicorn Application Cluster)
* **Componente:** Gunicorn ejecutándose sobre el entorno virtual (`.venv`).
* **Operación:**
  * Enlace exclusivo en interfaz local (`127.0.0.1:8000`) sin exposición directa hacia la red externa.
  * Cluster de procesos workers síncronos gestionados por un proceso Master.
  * Reciclado automático de workers para prevención de fugas de memoria y control de concurrencia.

### Capa 4: Framework Django 6.1 (Lógica de Negocio y Seguridad)
* **Stack de Middlewares en Cascada:**
  1. `SecurityMiddleware`: Fuerza HTTPS y valida cabeceras seguras.
  2. `SessionMiddleware`: Gestión de sesiones mediante cookies seguras (`Secure`, `HttpOnly`, `SameSite=Lax`).
  3. `CsrfViewMiddleware`: Verificación de tokens de protección contra peticiones falsificadas.
  4. `AuthenticationMiddleware`: Asociación de la identidad del usuario a cada solicitud HTTP.
  5. `AuditlogMiddleware`: Captura transaccional de IP del cliente, usuario y campos alterados.
* **Desacoplamiento Operativo:**
  * Gestión de secretos mediante `python-decouple` (`config()`).
  * Inexistencia de claves en código duro; archivo `.env` excluido del repositorio Git.
  * Entorno de producción certificado con `DEBUG = False`.

### Capa 5: Motor de Persistencia y Concurrencia (SQLite en Modo WAL)
* **Motor:** SQLite 3 (`db.sqlite3`).
* **Optimización de Alta Concurrencia:**
  * Modo **WAL (Write-Ahead Logging)** activado mediante la señal `connection_created` (`PRAGMA journal_mode=WAL;`).
  * Tolerancia a contención de concurrencia mediante `PRAGMA busy_timeout=5000;` (5 segundos de espera antes de error de bloqueo).
  * Permite múltiples lectores simultáneos (doctores consultando expedientes) concurrentes con escritores (recepción cobrando o doctor guardando nota médica).
* **Protección a Nivel Sistema de Archivos:**
  * Permisos restrictivos `chmod 600` sobre `db.sqlite3`, `db.sqlite3-wal` y `db.sqlite3-shm`.
  * Script automatizado [scripts/backup_db.sh](file:///c:/Users/Zephyrus/Desktop/practica/DentalSecureLab/scripts/backup_db.sh) para respaldo en caliente consistente vía `.backup` y cifrado simétrico **GPG AES-256**.

---

## 4. ARQUITECTURA DE MÓDULOS DE DOMINIO (APPS)

La plataforma está estructurada en módulos independientes y altamente cohesivos bajo el patrón MVT (Modelo - Vista - Template):

```
DentalSecureLab/
├── config/             # Orquestador del proyecto (settings.py, urls.py, wsgi.py)
├── core/               # Dashboard métrico, vista general y señales SQLite WAL
├── users/              # Autenticación, UserProfile (RBAC) y LoginAttemptTracker
├── patients/           # Maestro de pacientes y datos demográficos
├── agenda/             # Agendamiento, calendario y control de citas
├── records/            # Expedientes clínicos con identificador criptográfico UUID v4
├── payments/           # Registro de cobros, métodos de pago y validación CSRF
├── deploy/             # Configuraciones perimetrales de Nginx
├── scripts/            # Scripts de respaldo cifrado y utilidades operativas
└── docs/               # Documentación técnica, manuales y líneas base
```

### Detalle de Módulos y Controles Específicos:

| Módulo | Entidades Clave | Responsabilidad de Dominio | Controles de Seguridad Asociados |
| :--- | :--- | :--- | :--- |
| **`users`** | `User`, `UserProfile`, `LoginAttemptTracker` | Autenticación, asignación de roles y control de acceso. | Bloqueo progresivo de login (alerta en intento 2, bloqueo temporal de 5 min en intento 5 y de 30 min tras reincidencia). |
| **`records`** | `MedicalRecord` | Historial médico, diagnósticos, tratamientos y notas clínicas. | Identificador UUID v4 (neutraliza IDOR/BOLA). Restringido exclusivamente a roles `doctor` y `admin`. Auditado por `django-auditlog`. |
| **`payments`** | `Payment` | Transacciones de caja, montos, métodos de pago y recibos. | Protección estricta con token CSRF en formulario. Restringido para personal médico (exclusivo de `receptionist` y `admin`). |
| **`agenda`** | `Appointment` | Programación, confirmación y reprogramación de citas. | Validación de relaciones de clave foránea con pacientes y control de estados de cita. |
| **`patients`** | `Patient` | Registro maestro, datos demográficos y contacto. | Base relacional compartida protegida contra accesos anónimos mediante `@login_required`. |
| **`core`** | N/A (Vistas y Señales) | Panel de control central y configuración de conexión a BD. | Inyección de PRAGMAs WAL y agregación de indicadores clínicos según rol autenticado. |

---

## 5. MODELO DE DATOS Y ESQUEMA ENTIDAD-RELACIÓN

El modelo de datos relacional asegura la integridad referencial y la estricta vinculación de expedientes mediante identificadores pseudoaleatorios impredecibles:

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

## 6. FLUJO DE DATOS Y CICLO DE VIDA DE UNA PETICIÓN

El procesamiento de cualquier solicitud en DentalSecureLab sigue un pipeline riguroso y auditable:

```
[Cliente en Consultorio] (Navegador Web)
           │
           │  1. Petición HTTPS (TLS v1.3)
           ▼
[Nginx Reverse Proxy]
           │  2. Inspección TLS, cabeceras HSTS y redirección 301
           │  3. Proxy hacia 127.0.0.1:8000 con X-Forwarded-Proto
           ▼
[Gunicorn WSGI Server]
           │  4. Distribución a Worker síncrono activo
           ▼
[Django Middleware Pipeline]
           │  5. SecurityMiddleware: Validación de canal seguro
           │  6. SessionMiddleware: Carga de sesión segura
           │  7. CsrfViewMiddleware: Comprobación de token CSRF
           │  8. AuthenticationMiddleware: Carga de request.user
           │  9. AuditlogMiddleware: Captura de IP y Usuario
           ▼
[Controlador / Vista] (e.g. record_detail)
           │  10. Verificación RBAC (@login_required, request.user.role)
           │  11. Consulta por UUID v4 en MedicalRecord (Evita IDOR)
           ▼
[Django ORM]
           │  12. Señal connection_created aplica PRAGMA journal_mode=WAL
           ▼
[SQLite 3 Engine] (db.sqlite3)
           │  13. Lectura concurrente en db.sqlite3-wal sin bloquear escritores
           ▼
[Plantilla HTML]
           │  14. Renderizado seguro con escape contextual automático de variables
           ▼
[Respuesta HTTP] (Status 200 / Cookies HttpOnly + Secure + SameSite=Lax)
```

---

## 7. SEGMENTACIÓN DE RED Y TOPOLOGÍA FÍSICA

Conforme a la norma internacional **IEEE 802.1Q**, la red física de la clínica está segmentada en dos redes lógicas estancas administradas mediante switches de capa 2/3:

```
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

* **Regla Estricta Inter-VLAN:** Queda bloqueado todo enrutamiento entre la VLAN 20 y la VLAN 10. Ningún dispositivo personal de un paciente puede enviar paquetes ni resolver puertos hacia el servidor clínico.
* **Gabinete Rack Físico:** Todo el hardware neurálgico (switch, router, patch panel y servidor) reside dentro de un rack metálico cerrado bajo llave de acero laminado para impedir sabotajes físicos o extracción de medios de almacenamiento.