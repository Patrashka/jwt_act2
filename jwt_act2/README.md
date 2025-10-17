# Sistema de Autenticación JWT con Flask, MariaDB y Redis

Este proyecto implementa un sistema completo de autenticación JWT con Flask, incluyendo persistencia de usuarios, auditoría de tokens, refresh seguro con revocación, blocklist y bitácora de uso. **NUEVA VERSIÓN**: Incluye Redis como almacén de estado para comparación de rendimiento.

## Características

### Funcionalidades Base
- ✅ Autenticación JWT con access y refresh tokens
- ✅ Persistencia de usuarios en MariaDB
- ✅ Sistema de blocklist para tokens revocados
- ✅ Refresh seguro con revocación
- ✅ Bitácora de uso y auditoría completa
- ✅ CORS habilitado
- ✅ Validaciones de seguridad
- ✅ Logging detallado

### Nuevas Funcionalidades (Redis)
- ✅ **Redis como almacén de estado** para refresh/revocación
- ✅ **Endpoints paralelos** `/api-sql` y `/api-redis`
- ✅ **Medición de tiempos** de respuesta en milisegundos
- ✅ **Comparación de rendimiento** entre SQL y Redis
- ✅ **Sesiones en Redis** con TTL automático
- ✅ **Auditoría dual** (SQL + Redis)
- ✅ **Health check** para ambos sistemas

## Requisitos

- Python 3.7+
- MariaDB 10.3+
- Redis 6.0+
- pip

## 🚀 Instalación Rápida con Docker (Recomendado)

### Requisitos Previos
- Docker Desktop instalado y en ejecución
- Python 3.7+

### Pasos de Instalación

1. **Instalar dependencias Python:**
```bash
pip install -r requirements.txt
```

2. **Iniciar servicios con Docker:**
```bash
# Iniciar MariaDB
docker run -d --name mariadb-jwt \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=jwt_auth_db \
  -p 3306:3306 \
  mariadb:10.6

# (Opcional) Iniciar Redis - Si no lo haces, se usará el simulador en memoria
docker run -d --name redis-jwt \
  -p 6379:6379 \
  redis:7-alpine
```

3. **Ejecutar la aplicación:**
```bash
python app.py
```

4. **Verificar que todo funciona:**
```bash
curl http://localhost:5000/api/health
```

**Nota**: Si Redis no está disponible, el sistema usa automáticamente un simulador en memoria. ¡No hay problema!

## Instalación

### Opción 1: MariaDB Local (Alternativa)

#### Windows:
1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd parcial2
```

2. **Ejecutar script de inicio (recomendado):**
```bash
start_windows.bat
```

O manualmente:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python setup_windows.py

# Ejecutar aplicación
python app.py
```

#### Linux/Mac:
1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd parcial2
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar MariaDB:**
   - Instalar MariaDB localmente
   - Crear usuario root con contraseña (por defecto: `password`)
   - Asegurarse de que MariaDB esté ejecutándose en el puerto 3306

4. **Configurar variables de entorno:**
   - Editar `config.py` con tus credenciales de base de datos
   - Cambiar `JWT_SECRET_KEY` por una clave segura en producción

5. **Configurar base de datos:**
```bash
python setup_database.py
```


## Uso

1. **Ejecutar la aplicación:**
```bash
python app.py
```

2. **La aplicación estará disponible en:**
   - **API Base:** `http://localhost:5000/api`
   - **Health Check:** `http://localhost:5000/api/health`

3. **Probar la API:**
   - **Postman (Recomendado):** Usa la colección incluida en `postman_collection.json`
   - **Guía de Postman:** Consulta `GUIA_POSTMAN.md` para instrucciones detalladas

4. **Usuario de ejemplo:**
   - Username: `admin`
   - Password: `admin123`

## 🚀 Pruebas con Postman

El sistema incluye una colección completa de Postman para probar todas las funcionalidades de la API de forma profesional.

### Características de la Colección:

- **📝 Registro de usuarios** - Endpoint para crear nuevos usuarios
- **🔑 Login/Logout** - Autenticación con tokens JWT
- **👤 Gestión de perfil** - Ver información del usuario autenticado
- **🔄 Renovación de tokens** - Refresh automático de access tokens
- **📊 Auditoría** - Visualización de bitácora de uso
- **🔧 Utilidades** - Verificación de estado y health check
- **📋 Variables de entorno** - Configuración automática de tokens
- **🎯 Tests automáticos** - Validación de respuestas

### Cómo usar Postman:

1. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

2. **Importa la colección:**
   - Abre Postman
   - Importa `postman_collection.json`
   - Importa `postman_environment.json`

3. **Prueba las funcionalidades:**
   - Haz login con `admin` / `admin123`
   - Los tokens se guardan automáticamente
   - Prueba todos los endpoints autenticados
   - Ve la bitácora de auditoría

## Endpoints de la API

### Autenticación

#### POST `/api/register`
Registrar nuevo usuario.

**Request:**
```json
{
    "username": "usuario",
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
}
```

**Response:**
```json
{
    "message": "Usuario registrado exitosamente",
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "usuario@ejemplo.com",
        "is_active": true
    }
}
```

#### POST `/api/login`
Iniciar sesión.

**Request:**
```json
{
    "username": "usuario",
    "password": "contraseña123"
}
```

**Response:**
```json
{
    "message": "Login exitoso",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "usuario@ejemplo.com",
        "is_active": true
    }
}
```

#### POST `/api/refresh`
Renovar access token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
    "message": "Token renovado exitosamente",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST `/api/logout`
Cerrar sesión (revocar token actual).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "message": "Logout exitoso"
}
```

#### POST `/api/logout-all`
Cerrar todas las sesiones del usuario.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "message": "Todas las sesiones cerradas exitosamente"
}
```

### Perfil de Usuario

#### GET `/api/profile`
Obtener perfil del usuario autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "usuario@ejemplo.com",
        "is_active": true
    }
}
```

### Auditoría

#### GET `/api/audit-log`
Obtener bitácora de auditoría del usuario.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `limit`: Número máximo de registros (default: 50)

**Response:**
```json
{
    "audit_log": [
        {
            "id": 1,
            "user_id": 1,
            "action": "login",
            "token_jti": null,
            "ip_address": "127.0.0.1",
            "user_agent": "Mozilla/5.0...",
            "created_at": "2024-01-01T12:00:00"
        }
    ]
}
```

#### GET `/api/admin/audit-log`
Obtener bitácora de auditoría general (admin).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `limit`: Número máximo de registros (default: 100)

### Utilidades

#### GET `/api/health`
Verificar estado de la aplicación.

**Response:**
```json
{
    "status": "healthy",
    "database": "connected",
    "redis": "connected",
    "timestamp": "2024-01-01T12:00:00"
}
```

## 🚀 Endpoints Redis (Nuevos)

### Autenticación con Redis

#### POST `/api-redis/login`
Iniciar sesión usando Redis para almacenar estado.

**Request:**
```json
{
    "username": "usuario",
    "password": "contraseña123"
}
```

**Response:**
```json
{
    "message": "Login exitoso (Redis)",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "usuario@ejemplo.com",
        "is_active": true
    },
    "response_time_ms": 15.23
}
```

#### POST `/api-redis/refresh`
Renovar access token usando Redis.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
    "message": "Token renovado exitosamente (Redis)",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "response_time_ms": 8.45
}
```

#### POST `/api-redis/logout`
Cerrar sesión usando Redis.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "message": "Logout exitoso (Redis)",
    "response_time_ms": 12.67
}
```

#### POST `/api-redis/logout-all`
Cerrar todas las sesiones del usuario usando Redis.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "message": "Todas las sesiones cerradas exitosamente (Redis)",
    "response_time_ms": 18.92
}
```

### Auditoría con Redis

#### GET `/api-redis/audit-log`
Obtener bitácora de auditoría del usuario desde Redis.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "audit_log": [
        {
            "user_id": 1,
            "action": "login",
            "token_jti": null,
            "ip_address": "127.0.0.1",
            "user_agent": "Mozilla/5.0...",
            "created_at": "2024-01-01T12:00:00"
        }
    ],
    "response_time_ms": 5.34
}
```

#### GET `/api-redis/admin/audit-log`
Obtener bitácora de auditoría general desde Redis.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "audit_log": [...],
    "response_time_ms": 7.89
}
```

## 📊 Comparación de Rendimiento

#### POST `/api/performance/compare`
Comparar rendimiento entre SQL y Redis.

**Request:**
```json
{
    "username": "usuario",
    "password": "contraseña123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "usuario@ejemplo.com",
        "is_active": true
    },
    "comparison": {
        "sql": {
            "success": true,
            "response_time_ms": 25.67,
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        },
        "redis": {
            "success": true,
            "response_time_ms": 12.34,
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
    },
    "performance_analysis": {
        "faster_system": "redis",
        "time_difference_ms": -13.33,
        "percentage_difference": -51.9,
        "redis_advantage": "Redis es 51.9% más rápido que SQL"
    }
}
```

## Estructura de la Base de Datos

### Tabla `users`
- `id`: ID único del usuario
- `username`: Nombre de usuario único
- `email`: Email único
- `password_hash`: Hash de la contraseña (bcrypt)
- `is_active`: Estado del usuario
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

### Tabla `revoked_tokens`
- `id`: ID único del registro
- `jti`: JWT ID del token revocado
- `token_type`: Tipo de token (access/refresh)
- `user_id`: ID del usuario propietario
- `revoked_at`: Fecha de revocación
- `expires_at`: Fecha de expiración del token

### Tabla `token_audit`
- `id`: ID único del registro
- `user_id`: ID del usuario
- `action`: Acción realizada (login/logout/refresh/revoke)
- `token_jti`: JWT ID del token (opcional)
- `ip_address`: Dirección IP del cliente
- `user_agent`: User Agent del cliente
- `created_at`: Fecha de la acción

## Configuración

### Variables de Entorno (config.py)

```python
# Base de datos
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'jwt_auth_db'

# JWT
JWT_SECRET_KEY = 'your-super-secret-jwt-key'
JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutos
JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 días

# Aplicación
FLASK_ENV = 'development'
FLASK_DEBUG = True
```

## Seguridad

- Contraseñas hasheadas con bcrypt
- Tokens JWT con expiración configurable
- Sistema de blocklist para tokens revocados
- Validación de entrada en todos los endpoints
- Logging de todas las acciones de autenticación
- CORS configurado para desarrollo

## Desarrollo

### Estructura del Proyecto

```
parcial2/
├── app.py                      # Aplicación principal Flask
├── config.py                   # Configuración para MariaDB local
├── database.py                 # Conexión y gestión de base de datos
├── models.py                   # Modelos de datos
├── setup_windows.py            # Script de configuración de BD (Windows)
├── start_windows.bat           # Script de inicio para Windows
├── requirements.txt            # Dependencias Python
├── postman_collection.json     # Colección de Postman
├── postman_environment.json    # Variables de entorno de Postman
├── GUIA_POSTMAN.md            # Guía detallada para usar Postman
└── README.md                  # Documentación
```

### Logs

La aplicación registra todas las acciones importantes:
- Conexiones a base de datos
- Registros de usuarios
- Inicios de sesión
- Renovaciones de tokens
- Cierres de sesión
- Errores del sistema

## Producción

Para usar en producción:

1. Cambiar `JWT_SECRET_KEY` por una clave segura
2. Configurar `FLASK_DEBUG = False`
3. Usar un servidor WSGI como Gunicorn
4. Configurar HTTPS
5. Usar variables de entorno para configuración sensible
6. Implementar rate limiting
7. Configurar backup de base de datos

## Troubleshooting

### Error de conexión a MariaDB
- Verificar que MariaDB esté ejecutándose
- Comprobar credenciales en `config.py`
- Verificar que el puerto 3306 esté disponible

### Error de JWT
- Verificar que `JWT_SECRET_KEY` esté configurado
- Comprobar que los tokens no hayan expirado
- Verificar que el token no esté en la blocklist

### Error de permisos
- Verificar que el usuario de base de datos tenga permisos para crear tablas
- Comprobar que la base de datos `jwt_auth_db` pueda ser creada

### Scripts de utilidad
- `python setup_windows.py`: Configurar base de datos (Windows)
- `start_windows.bat`: Script de inicio completo para Windows
- `postman_collection.json`: Colección de Postman para probar la API
- `GUIA_POSTMAN.md`: Guía detallada para usar Postman
