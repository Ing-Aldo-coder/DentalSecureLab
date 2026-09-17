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

## 🏗️ Arquitectura del laboratorio

El laboratorio está pensado para trabajar en equipos de dos estudiantes.

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

Durante las primeras etapas del proyecto, DentalSecureLab se instala y configura en **Ubuntu Server**.

Posteriormente, el segundo equipo podrá utilizar herramientas de análisis y pentesting desde **Kali Linux** para evaluar la infraestructura dentro de un entorno autorizado y controlado.

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

```mermaid
flowchart TD

subgraph group_runtime["Django Runtime"]
  node_manage["Django command entry<br/>Python CLI<br/>[manage.py]"]
  node_settings["Runtime settings<br/>Django configuration<br/>[settings.py]"]
  node_adapters["WSGI / ASGI adapters<br/>Django server adapters<br/>[wsgi.py]"]
  node_router["Project URL dispatcher<br/>Django routing<br/>[urls.py]"]
  node_shared_ui["Shared dashboard UI<br/>HTML / CSS templates<br/>[dashboard.html]"]
  node_sqlite[("Local SQLite database<br/>persistent datastore")]
end

subgraph group_apps["Domain Apps"]
  node_dashboard["Core dashboard<br/>aggregation views<br/>[views.py]"]
  node_patients[("Patient master data<br/>Django models, forms, views<br/>[models.py]")]
  node_agenda["Scheduling<br/>appointment models and views<br/>[models.py]"]
  node_records[("Clinical records<br/>medical-record models and views<br/>[models.py]")]
  node_record_uuid_migration["Record UUID migration<br/>Django migration"]
  node_payments[("Payments<br/>payment models, forms, views<br/>[models.py]")]
  node_identity["Authentication &amp; users<br/>user models and views<br/>[models.py]"]
  node_login_tracker["Login attempt tracking<br/>security migration"]
end

subgraph group_security["Security &amp; Operations"]
  node_nginx["Nginx reverse proxy<br/>deployment gateway"]
  node_backup["Database backup<br/>operations script<br/>[backup_db.sh]"]
  node_security_guidance["Hardening &amp; audit guidance<br/>security documentation"]
  node_assessment_lab["Authorized assessment lab"]
end

node_manage -->|"loads"| node_settings
node_manage -->|"migrates"| node_sqlite
node_nginx -->|"proxies requests to"| node_adapters
node_adapters -->|"serves"| node_router
node_router -->|"routes to"| node_dashboard
node_router -->|"routes to"| node_patients
node_router -->|"routes to"| node_agenda
node_router -->|"routes to"| node_records
node_router -->|"routes to"| node_payments
node_router -->|"routes to"| node_identity
node_dashboard -->|"renders"| node_shared_ui
node_dashboard -.->|"summarizes"| node_patients
node_dashboard -.->|"summarizes"| node_agenda
node_dashboard -.->|"summarizes"| node_records
node_dashboard -.->|"summarizes"| node_payments
node_agenda -->|"appointments belong to"| node_patients
node_records -->|"records belong to"| node_patients
node_record_uuid_migration -->|"evolves identifier"| node_records
node_identity -->|"records attempts via"| node_login_tracker
node_patients -->|"persists"| node_sqlite
node_agenda -->|"persists"| node_sqlite
node_records -->|"persists"| node_sqlite
node_payments -->|"persists"| node_sqlite
node_identity -->|"persists"| node_sqlite
node_backup -->|"backs up"| node_sqlite
node_security_guidance -.->|"guides hardening"| node_nginx
node_assessment_lab -.->|"assesses authorized exposure"| node_nginx

click node_manage "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/manage.py"
click node_settings "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/config/settings.py"
click node_adapters "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/config/wsgi.py"
click node_router "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/config/urls.py"
click node_shared_ui "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/templates/dashboard.html"
click node_dashboard "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/core/views.py"
click node_patients "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/patients/models.py"
click node_agenda "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/agenda/models.py"
click node_records "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/records/models.py"
click node_record_uuid_migration "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/records/migrations/0002_medicalrecord_uuid.py"
click node_payments "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/payments/models.py"
click node_identity "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/users/models.py"
click node_login_tracker "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/users/migrations/0002_loginattempttracker.py"
click node_nginx "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/deploy/nginx/dentalsecurelab.conf"
click node_backup "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/scripts/backup_db.sh"
click node_security_guidance "https://github.com/ing-aldo-coder/dentalsecurelab/blob/main/docs/network_hardening.md"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_manage,node_settings,node_adapters,node_router,node_shared_ui,node_sqlite toneBlue
class node_dashboard,node_patients,node_agenda,node_records,node_record_uuid_migration,node_payments,node_identity,node_login_tracker toneAmber
class node_nginx,node_backup,node_security_guidance,node_assessment_lab toneMint
```