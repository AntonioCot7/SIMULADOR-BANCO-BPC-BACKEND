# Simulador de Banco BPC - Backend 🏦💻

Este repositorio contiene el **backend** de un simulador de banco llamado **BPC**, creado utilizando servicios de AWS y **Serverless Framework**. El backend incluye microservicios implementados en **Python** y **Node.js**, con diferentes funcionalidades relacionadas con usuarios, cuentas bancarias, transacciones, pagos, préstamos, soporte, etc.

El backend se utiliza para gestionar los datos y la lógica de negocio del simulador, y está estructurado para ser desplegado fácilmente en diferentes entornos utilizando **AWS Lambda**, **API Gateway** y **DynamoDB**.

## Repositorio 📦

**GitHub**: [Simulador Banco BPC Backend](https://github.com/AntonioCot7/SIMULADOR-BANCO-BPC-BACKEND.git)

---

## Requisitos 🔧

- **AWS Account** con permisos para usar Lambda, API Gateway, DynamoDB y otros servicios de AWS.
- **Node.js** y **npm** instalados para gestionar las dependencias de los microservicios en Node.js.
- **Python** y **pip** instalados para gestionar las dependencias de los microservicios en Python.
- **Serverless Framework** instalado para desplegar los microservicios.

---

## Descripción de los Microservicios 💡

El sistema está dividido en varios microservicios, organizados en dos categorías: **Python** y **Node.js**.

### Microservicios en Python 🐍:

1. **TABLA-USUARIO**: Información de los usuarios del sistema.
2. **TABLA-TOKENS**: Almacena los tokens de acceso para la autenticación.
3. **TABLA-CUENTAS**: Información de las cuentas bancarias de los usuarios.
4. **TABLA-TARJETAS**: Información de las tarjetas asociadas a las cuentas.
5. **TABLA-TRANSACCION**: Registra las transacciones entre cuentas.
6. **TABLA-PAGOS**: Registra los pagos realizados por los usuarios.

### Microservicios en Node.js 🌐:

1. **TABLA-SOPORTE**: Almacena los tickets de soporte creados por los usuarios.
2. **TABLA-SOLICITUD-PRESTAMO**: Almacena las solicitudes de préstamos.
3. **TABLA-PRESTAMO**: Almacena los préstamos otorgados a los usuarios.

---

## Detalles de las Tablas 📊

### **Python** 🐍

#### 🏷️ **TABLA TOKENS_ACCESO**
- **Descripción:** Almacena los tokens de acceso de los usuarios.
- **Campos:**
  - `token` – Token de acceso generado.
  - `expires` – Fecha de expiración del token.

#### 👤 **TABLA USUARIOS**
- **Descripción:** Contiene la información de los usuarios registrados.
- **Campos:**
  - `usuario_id` – Identificador único del usuario.
  - `nombre` – Nombre del usuario.
  - `apellido` – Apellido del usuario.
  - `email` – Correo electrónico del usuario.
  - `password` – Contraseña del usuario.
  - `teléfono` – Número de teléfono.
  - `dni` – Documento de identidad del usuario.
  - `dirección` – Dirección del usuario.
  - `fecha_nac` – Fecha de nacimiento del usuario.

#### 🏦 **TABLA CUENTAS**
- **Descripción:** Almacena las cuentas bancarias de los usuarios.
- **Campos:**
  - `usuario_id` – Identificador del usuario.
  - `cuenta_id` – Identificador único de la cuenta bancaria.
  - `cuenta_datos` – Información de la cuenta, como saldo, nombre y tipo de interés.

#### 💳 **TABLA TARJETAS**
- **Descripción:** Contiene la información de las tarjetas asociadas a las cuentas bancarias.
- **Campos:**
  - `cuenta_id` – Identificador de la cuenta bancaria asociada.
  - `tarjeta_id` – Identificador único de la tarjeta.
  - `tarjeta_datos` – Información de la tarjeta, como saldo disponible, estado, fechas y CVV.

#### 💸 **TABLA PAGOS**
- **Descripción:** Registra los pagos realizados por los usuarios.
- **Campos:**
  - `usuario_id` – Identificador del usuario que realiza el pago.
  - `pago_id` – Identificador único del pago.
  - `título` – Título o descripción del pago.
  - `descripción` – Descripción detallada del pago.
  - `tipo` – Tipo de pago.
  - `estado` – Estado del pago.
  - `fecha` – Fecha en la que se realizó el pago.

#### 🔄 **TABLA TRANSACCION**
- **Descripción:** Almacena las transacciones realizadas entre cuentas bancarias.
- **Campos:**
  - `cuenta_origen` – Cuenta de origen de la transacción.
  - `transaccion_id` – Identificador único de la transacción.

---

### **Node.js** 🌐

#### 🛠️ **TABLA SOPORTE**
- **Descripción:** Almacena los tickets de soporte creados por los usuarios.
- **Campos:**
  - `usuario_id` – Identificador del usuario que creó el ticket.
  - `ticket_id` – Identificador único del ticket de soporte.
  - `tipo` – Tipo de solicitud o problema.
  - `estado` – Estado actual del ticket.
  - `descripción` – Descripción del problema.
  - `fecha_creación` – Fecha de creación del ticket.

#### 💰 **TABLA SOLICITUD PRESTAMO**
- **Descripción:** Almacena las solicitudes de préstamos realizadas por los usuarios.
- **Campos:**
  - `usuario_id` – Identificador del usuario que solicitó el préstamo.
  - `solicitud_id` – Identificador único de la solicitud.
  - `título` – Título de la solicitud.
  - `descripción` – Descripción detallada del préstamo solicitado.
  - `tipo` – Tipo de préstamo solicitado.
  - `estado` – Estado de la solicitud.
  - `fecha` – Fecha de la solicitud.

#### 💸 **TABLA PRESTAMO**
- **Descripción:** Almacena información sobre los préstamos otorgados a los usuarios.
- **Campos:**
  - `usuario_id` – Identificador del usuario que recibió el préstamo.
  - `prestamo_id` – Identificador único del préstamo.
  - `título` – Título del préstamo.
  - `descripción` – Descripción del préstamo otorgado.
  - `tipo` – Tipo de préstamo.
  - `estado` – Estado del préstamo.
  - `fecha` – Fecha en que se otorgó el préstamo.

---

## Arquitectura 🏗️

La arquitectura se basa en **microservicios independientes** que se comunican entre sí a través de **API Gateway** y utilizan **AWS Lambda** para procesar las solicitudes. Los datos se almacenan en **DynamoDB**, utilizando tablas específicas para cada microservicio.

![Arquitectura Solución](imagen_referencial_de_arquitectura.png)

---

## Seguridad 🔒

El backend implementa un sistema de seguridad basado en tokens para la autenticación y autorización de los usuarios. El flujo de seguridad es el siguiente:

1. **Recepción de la solicitud**: El microservicio recibe una solicitud HTTP con un token de acceso en el cuerpo de la solicitud.
2. **Validación del cuerpo**: Si el cuerpo de la solicitud es incorrecto, se devuelve un error 400 (Solicitud Inválida).
3. **Verificación del token**: El token se busca en la tabla `TABLA-TOKENS_ACCESO` en DynamoDB.
4. **Verificación de expiración**: Si el token ha expirado, se devuelve un error 403 (Token expirado).
5. **Respuesta positiva**: Si el token es válido y no ha expirado, el microservicio devuelve el `usuario_id` asociado al token.

---

# Pasos para desplegar los servicios 📦

# 1. Clona el repositorio desde GitHub 🖥️
echo "Clonando el repositorio..."
git clone https://github.com/AntonioCot7/SIMULADOR-BANCO-BPC-BACKEND.git
cd SIMULADOR-BANCO-BPC-BACKEND

# 2. Navega a la carpeta Deploy y selecciona el script correspondiente al entorno 🌍

# Para desarrollo (dev) 🛠️
echo "Desplegando en el entorno de desarrollo (dev)..."
sh scripts/deploy-dev.sh

# Para pruebas (test) 🧪
echo "Desplegando en el entorno de pruebas (test)..."
sh scripts/deploy-test.sh

# Para producción (prod) 🌟
echo "Desplegando en el entorno de producción (prod)..."
sh scripts/deploy-prod.sh

# Durante el despliegue ⚙️

# 3. Instalación de dependencias automáticamente para servicios en Node.js 🚀
echo "Instalando dependencias..."
npm install  # Incluye uuid y aws-sdk

# 4. Despliegue de cada microservicio utilizando serverless deploy 🔥
echo "Desplegando microservicios con Serverless..."
npx serverless deploy --stage <STAGE>

# 5. Verifica los recursos desplegados en AWS y las conexiones entre microservicios 🛠️🌐
echo "Verificando recursos en AWS..."
# Aquí podrías agregar comandos para hacer esta verificación

# Para eliminar recursos 🔥🚮

# 6. Elimina los recursos de un entorno específico cuando ya no sean necesarios 💥

# Usa los scripts correspondientes para eliminar los recursos del entorno elegido

# Para desarrollo (dev) 🧹
echo "Eliminando recursos del entorno de desarrollo (dev)..."
sh scripts/remove-dev.sh

# Para pruebas (test) 🧽
echo "Eliminando recursos del entorno de pruebas (test)..."
sh scripts/remove-test.sh

# Para producción (prod) 🧨
echo "Eliminando recursos del entorno de producción (prod)..."
sh scripts/remove-prod.sh

# Postman Collection 📬

# 7. El archivo de colección de Postman está configurado para el entorno dev, pero se puede usar también en prod o test 🌟
echo "Asegúrate de tener el archivo de colección de Postman correctamente configurado."

# Recursos adicionales 📚

# 8. Accede a los spreadsheets con detalles de las tablas y atributos (PK, SK, GSI, LSI):
echo "Consulta las especificaciones de las tablas en el siguiente enlace:"
echo "Especificación de Tablas, esto es un link." 🔗

