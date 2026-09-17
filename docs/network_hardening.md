# POLÍTICA DE ENDURECIMIENTO DE INFRAESTRUCTURA DE RED, RACK Y SEGMENTACIÓN POR VLAN
**Clínica Odontológica Especializada DentalSecureLab**  
**Código Normativo:** POL-NET-SEC-02 | **Versión:** 1.0 Oficial  
**Clasificación:** Confidencial / Uso Interno de Infraestructura y TI  

---

## 1. OBJETIVO Y ALCANCE DE LA SEGURIDAD EN CAPA DE RED

La presente directiva técnica tiene por objetivo blindar la infraestructura física y lógica de telecomunicaciones de DentalSecureLab, mitigando de forma integral los riesgos de interrupción de servicio, accesos no autorizados mediante conexiones inalámbricas y manipulación directa del hardware de red.
Esta normativa abarca la totalidad de los equipos de telecomunicaciones que conforman la topología de la clínica, incluyendo el enrutador perimetral de borde, los switches gestionables de capa 2/3, los puntos de acceso inalámbricos (WAP), el cableado estructurado Categoría 6A y el gabinete de comunicaciones ubicado en el área técnica.
El cumplimiento de este estándar es mandatorio para el Administrador de Sistemas y TI, así como para cualquier proveedor o contratista externo autorizado que realice labores de soporte o mantenimiento de cableado estructurado en las instalaciones.
La implementación garantiza la continuidad operativa y la confidencialidad de las transmisiones de datos generadas desde los cuatro consultorios odontológicos y la recepción hacia el servidor local de la plataforma clínica.

---

## 2. POLÍTICA DE PROTECCIÓN FÍSICA Y AISLAMIENTO EN RACK CERRADO

Todos los dispositivos centrales de telecomunicaciones, el servidor local de DentalSecureLab, el sistema de alimentación ininterrumpida (UPS) y los paneles de parcheo deben residir exclusivamente dentro de un gabinete rack cerrado bajo llave de acero laminado fijado rígidamente a muro estructural.
El acceso físico al gabinete de comunicaciones queda estrictamente restringido al Administrador de TI y a la Dirección General de la clínica, manteniendo la llave física resguardada bajo caja de seguridad con combinación mecánica no compartida.
Queda expresamente prohibido dejar la compuerta frontal o los paneles laterales del rack abiertos sin supervisión presencial continua durante labores de mantenimiento o diagnóstico de cableado de red.
Toda apertura del gabinete deberá ser registrada en la bitácora física de control de accesos al cuarto técnico, consignando nombre del operador, motivo técnico, fecha, hora de apertura y hora de cierre verificado.

```
+-----------------------------------------------------------------------------------+
|                        RACK CERRADO Y TOPOLOGÍA DE SEGURIDAD                      |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ GABINETE RACK CERRADO CON LLAVE FÍSICA Y ACCESO RESTRINGIDO ]                  |
|  +-----------------------------------------------------------------------------+  |
|  | [1] Router de Borde (WAN Mgmt OFF | Firewall SPI | DoS Protection)          |  |
|  | [2] Switch Gestionable Capa 2/3 (802.1Q VLANs | Port Security 802.1X)       |  |
|  | [3] Servidor DentalSecureLab (Debian GNU/Linux | Nginx TLS | Django WAL)    |  |
|  | [4] Unidad de Respaldo Eléctrico UPS Smart 1500VA (Autonomía 45 minutos)     |  |
|  +-----------------------------------------------------------------------------+  |
|         | (Troncal 802.1Q Tagged)                                                 |
|         +---------------------------------------+                                 |
|                                                 |                                 |
|   VLAN 10: MÉDICA Y ADMINISTRATIVA              | VLAN 20: PACIENTES E INVITADOS  |
|   Subred: 192.168.10.0/24 (CABLEADA)            | Subred: 192.168.20.0/24 (WIFI)  |
|   +---------------------------------------+     +-------------------------------+ |
|   | Consultorios 1 al 4 (5 Doctores + 1 E)|     | Sala de Espera (Pacientes)    | |
|   | Recepción (1 Terminal Cobro / Citas)  |     | Aislamiento de Clientes (AP)  | |
|   | Servidor DentalSecureLab:443          |     | BLOQUEO TOTAL HACIA VLAN 10   | |
|   +---------------------------------------+     +-------------------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 3. LÍNEA BASE DE CONFIGURACIÓN Y ENDURECIMIENTO DE ENRUTADORES Y SWITCHES

Los enrutadores y switches gestionables desplegados en la red clínica deben someterse a una configuración de endurecimiento (hardening baseline) previo a su conexión a la red de producción.
Queda estrictamente prohibido el uso de contraseñas de fábrica (`admin/admin`, `root/toor` o contraseñas por defecto del fabricante); las credenciales administrativas deben ser complejas, de al menos 16 caracteres alfanuméricos con símbolos, renovadas cada 90 días.
La interfaz de administración web a través del puerto WAN (Wide Area Network / Internet pública) debe permanecer permanentemente deshabilitada para imposibilitar ataques de escaneo o fuerza bruta provenientes del exterior.
Todos los protocolos inseguros en texto claro, incluyendo Telnet, HTTP en puerto 80, SNMP v1/v2c y TFTP, deben ser desactivados en su totalidad, forzando la administración local mediante SSH versión 2 con autenticación por clave pública RSA-4096 o Ed25519.
Los servicios no esenciales, tales como Wi-Fi Protected Setup (WPS), Universal Plug and Play (UPnP), descubrimiento CDP/LLDP no autorizado y redireccionamiento ICMP, deben ser anulados para reducir la superficie de ataque perimetral.

---

## 4. SEGMENTACIÓN LÓGICA DE RED POR VLAN (IEEE 802.1Q)

La arquitectura de red de DentalSecureLab implementa una segmentación obligatoria basada en redes de área local virtuales (VLANs) conforme al estándar internacional IEEE 802.1Q, separando drásticamente el tráfico clínico confidencial del acceso público a Internet.
Se establecen formalmente dos segmentos lógicos estancos y mutuamente aislados dentro del switch principal:
1. **VLAN 10 (Médica y Administrativa):** Asignada a los 4 consultorios odontológicos (médicos generales, especialistas y asistente), a la estación de recepción y al servidor de base de datos. Opera en el segmento privado `192.168.10.0/24` con direccionamiento estático por reserva DHCP ligada a dirección MAC.
2. **VLAN 20 (Invitados y Pacientes):** Asignada exclusivamente a la red inalámbrica de cortesía en la sala de espera bajo el SSID `DentalSecureLab_Invitados`. Opera en el segmento `192.168.20.0/24` mediante DHCP dinámico con ancho de banda regulado por QoS.

La tabla de control de conmutación del switch aplica reglas estrictas que impiden cualquier comunicación inter-VLAN entre la VLAN 20 y la VLAN 10.
Los dispositivos conectados a la red de invitados únicamente disponen de enrutamiento directo hacia la puerta de enlace a Internet, contando con la directiva *Client Isolation* activada en el punto de acceso para evitar que los teléfonos móviles de los pacientes se detecten entre sí.
El servidor DentalSecureLab se encuentra conectado exclusivamente al puerto físico asignado a la VLAN 10, siendo completamente invisible e inalcanzable para cualquier dispositivo ubicado en la VLAN de invitados.

---

## 5. REGLAS DE FIREWALL Y MONITOREO DE INTEGRIDAD DE RED

El enrutador y el firewall local del servidor implementan políticas de filtrado de paquetes bajo el principio de privilegio mínimo, denegando por defecto todo tráfico entrante no autorizado explícitamente (política `DROP by default`).
Únicamente se autorizan peticiones entrantes hacia el puerto HTTPS (443/TCP) provenientes del rango `192.168.10.0/24` de la VLAN Médica, descartando silenciosamente cualquier intento de conexión SSH originado fuera de la IP fija del administrador de TI.
Se activa el módulo de prevención de escaneo de puertos (Port Scan Protection) y limitación de tasa de paquetes SYN (SYN Flood Protection) para mitigar intentos de saturación o denegación de servicio que pretendan congelar las consultas clínicas concurrentes.
El Administrador de TI efectuará revisiones mensuales de las tablas de direcciones MAC registradas en los switches para detectar e investigar inmediatamente cualquier nodo no inventariado conectado físicamente a las tomas de red de los consultorios.
