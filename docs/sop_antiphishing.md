# PROCEDIMIENTO OPERATIVO ESTÁNDAR (SOP-SEC-01)
# PROTOCOLO DE PREVENCIÓN DE INGENIERÍA SOCIAL, PHISHING Y VERIFICACIÓN FUERA DE BANDA
**Clínica Odontológica Especializada DentalSecureLab**  
**Código Normativo:** SOP-SEC-01-2026 | **Versión:** 2.0 Oficial  
**Audiencia Obligatoria:** Recepción, Odontólogos Generales, Especialistas, Asistente Dental y Administrador TI.  

---

## 1. OBJETIVO Y ALCANCE INSTITUCIONAL

El presente Procedimiento Operativo Estándar tiene como propósito fundamental establecer las directrices técnicas, administrativas y de comportamiento humano necesarias para prevenir, detectar, mitigar y responder ante ataques cibernéticos basados en ingeniería social, campañas de phishing dirigido (spear-phishing), suplantación de identidad telefónica (vishing) y desvío fraudulento de fondos o expedientes de salud dentro de DentalSecureLab.
Este protocolo posee un carácter estrictamente obligatorio para la totalidad de la plantilla institucional, compuesta por los tres odontólogos generales de los consultorios 1 al 3, los dos especialistas odontológicos de ortodoncia y endodoncia del consultorio 4, el personal de enfermería y asistencia dental, la recepción general y la administración de tecnologías de la información.
Cualquier interacción digital o presencial que involucre la solicitud de credenciales, modificación de cuentas bancarias de proveedores, alteración de datos personales de pacientes o descarga de archivos adjuntos no solicitados deberá regirse indefectiblemente por las normas de control descritas en este documento institucional.
El alcance de este instrumento abarca todas las estaciones de trabajo fijas de los cuatro consultorios clínicos, la terminal de facturación y cobro en recepción, los dispositivos móviles institucionales y los canales de comunicación oficiales tales como correo electrónico corporativo, telefonía interna y mensajería cifrada autorizada.

---

## 2. ANÁLISIS DE AMENAZAS EN EL ENTORNO CLÍNICO-DENTAL

Los entornos de salud odontológica constituyen objetivos altamente atractivos para la delincuencia informática organizada debido a la coexistencia de información médica altamente confidencial y transacciones monetarias cotidianas procesadas con rapidez en el área de recepción.
Los vectores de ataque más recurrentes identificados en la clínica incluyen correos electrónicos fraudulentos simulando ser aseguradoras médicas o distribuidores dentales solicitando la descarga de supuestas facturas o expedientes en formatos ejecutables o macros de ofimática maliciosas.
Asimismo, el personal de recepción y los médicos generales se encuentran expuestos a intentos de persuasión psicológica donde atacantes externos fingen ser pacientes urgidos o auditores sanitarios gubernamentales solicitando contraseñas temporales o enlaces de acceso directo a la plataforma.
La presente política reconoce que la barrera técnica más sofisticada implementada en el servidor Django resulta vulnerable si el factor humano sucumbe ante engaños diseñados para vulnerar la confianza o explotar la premura en la atención médica asistencial.

---

## 3. PROTOCOLO DE VERIFICACIÓN FUERA DE BANDA (OUT-OF-BAND - OOB)

La verificación fuera de banda constituye la medida de control compensatorio más efectiva para invalidar cualquier intento de fraude en transacciones financieras o transferencias de datos sensibles ejecutadas mediante canales digitales susceptibles de suplantación.
Se define como verificación fuera de banda a la validación obligatoria de una instrucción o solicitud a través de un canal de comunicación totalmente independiente, seguro y previamente acordado, que difiera de forma absoluta del medio por el cual se recibió la petición inicial.
Queda estrictamente prohibido procesar cualquier solicitud de cambio de cuenta CLABE bancaria, modificación en el método de pago de proveedores de insumos dentales o remisión extraordinaria de expedientes clínicos recibida por correo electrónico sin completar el ciclo OOB.
El ciclo de verificación exige contactar de manera directa al emisor mediante una llamada telefónica a un número registrado previamente en el directorio corporativo oficial (nunca al número que figura al pie del correo sospechoso) y solicitar la confirmación verbal y presencial del responsable administrativo.

```
+-------------------------------------------------------------------------------+
|                      FLUJO DE VERIFICACIÓN FUERA DE BANDA                     |
+-------------------------------------------------------------------------------+
| 1. Recepción de Solicitud Crítica (Correo / SMS / Mensajería)                 |
|    - Cambio de cuenta de abono para proveedores dentales o laboratorios.      |
|    - Petición atípica de exportación masiva de expedientes o historiales.     |
+-------------------------------------------------------------------------------+
                                      |
                                      v
| 2. Bloqueo Preventivo Inmediato en Terminal DentalSecureLab                   |
|    - No pulsar enlaces, no descargar adjuntos, no responder al emisor.        |
|    - Pausar cualquier trámite administrativo o cobro en /payments/.           |
+-------------------------------------------------------------------------------+
                                      |
                                      v
| 3. Activación del Segundo Canal de Comunicación Independiente                 |
|    - Llamada de voz a número oficial certificado en el archivo físico.        |
|    - Cotejo mediante código de verificación verbal de 4 dígitos preacordado.  |
+-------------------------------------------------------------------------------+
                                      |
                     +----------------+----------------+
                     |                                 |
         [Validación Exitosa]                [Discrepancia o Sospecha]
                     |                                 |
                     v                                 v
        Proceder con la operación          Activar Protocolo de Incidente
        y registrar bitácora OOB.          y notificar a Administrador TI.
```

---

## 4. DIRECTIVAS ESPECÍFICAS PARA RECEPCIÓN Y COBROS

El personal de recepción, al ser el nodo primario de interacción financiera en los módulos de pacientes, citas y pagos (`/patients/`, `/agenda/`, `/payments/`), deberá abstenerse rigurosamente de abrir correos o enlaces provenientes de remitentes desconocidos en la computadora de cobro.
Bajo ninguna circunstancia la recepcionista proporcionará información personal, números telefónicos privados de los doctores ni registros de pagos a personas que llamen solicitando confirmaciones telefónicas no agendadas formalmente.
Si un paciente solicita un cambio en la modalidad de cobro o refiere que una transferencia bancaria fue efectuada a una cuenta distinta a la institucional de DentalSecureLab, el personal de recepción deberá solicitar el comprobante impreso oficial y dar parte al administrador de TI.
Todo recibo o comprobante emitido a través del módulo de pagos deberá ser generado y verificado exclusivamente desde la sesión autenticada de la recepcionista, cerrando la sesión mediante el botón superior cada vez que se retire de la ventanilla de atención.

---

## 5. DIRECTIVAS ESPECÍFICAS PARA ODONTÓLOGOS GENERALES Y ESPECIALISTAS

Los tres odontólogos generales y los dos especialistas de los consultorios clínicos operan estaciones fijas donde se visualizan expedientes clínicos y antecedentes patológicos altamente sensibles bajo el marco de la confidencialidad médica profesional.
Queda terminantemente prohibido a los médicos acceder a sus correos electrónicos personales, redes sociales, servicios de almacenamiento en la nube no corporativos o sitios web ajenos a la práctica odontológica desde los equipos clínicos de consulta.
En caso de recibir una radiografía, tomografía dental o interconsulta externa mediante correo electrónico, el archivo deberá ser validado previamente mediante el análisis del buzón centralizado antes de ser descargado o ejecutado en la terminal del consultorio.
Los especialistas deberán recordar que el software DentalSecureLab nunca solicitará su contraseña a través de ventanas emergentes en el navegador ni mediante mensajes de texto durante la edición o consulta de notas de evolución clínica.

---

## 6. MATRIZ DE IDENTIFICACIÓN DE SEÑALES DE ALERTA (RED FLAGS)

| Vector de Amenaza | Señal de Alerta Identificada | Acción Inmediata Requerida |
| :--- | :--- | :--- |
| Correo Electrónico | Dominio con discrepancia tipográfica (ej. `@dentalsecure-lab.com` o `@gmail.com`). | Reportar de inmediato a TI y marcar como correo no deseado sin abrir el contenido. |
| Adjuntos Sospechosos | Archivos comprimidos `.zip`, ejecutables `.exe`, documentos `.docm` con macros habilitadas. | Bloquear la descarga en la red local y no habilitar edición ni macros bajo ningún motivo. |
| Suplantación Telefónica | Llamadas urgentes exigiendo depósitos bancarios a nombre del director de la clínica. | Colgar de inmediato y verificar la identidad de manera presencial o vía extensión interna. |
| Códigos QR Falsificados | Adhesivos sobrepuestos en folletos de pago o carteles colocados en la sala de espera. | Retirar el adhesivo adulterado y notificar formalmente a recepción y administración. |
| Solicitud de Contraseña | Ventana o mensaje solicitando claves para "actualización obligatoria de seguridad". | Rechazar la solicitud; el personal de TI jamás solicita contraseñas operativas a usuarios. |

---

## 7. PROTOCOLO ANTE INCIDENTES DE SEGURIDAD Y ESCALAMIENTO

En el momento exacto en que cualquier miembro del equipo sospeche haber sido víctima de un engaño, haber introducido sus credenciales en un formulario falso o haber ejecutado un archivo con comportamiento anómalo, deberá proceder a la desconexión física inmediata del cable de red Ethernet.
Bajo ninguna circunstancia el usuario deberá intentar ocultar el incidente por temor a sanciones disciplinarias; la política institucional premia la notificación oportuna como factor primordial para la contención exitosa de cualquier brecha.
La notificación formal deberá realizarse de viva voz al Administrador del Sistema y TI en un lapso no mayor a 10 minutos posteriores al evento, indicando la hora exacta, el equipo afectado, el consultorio y la naturaleza del enlace o archivo interactuado.
El Administrador de TI procederá al restablecimiento inmediato de la contraseña comprometida en la base de datos de Django, la revocación de sesiones activas en la tabla `django_session` y la revisión de la bitácora de eventos mediante `django-auditlog`.
