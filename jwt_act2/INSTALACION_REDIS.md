# Instalación y Configuración de Redis

## 🚀 Instalación Rápida

### Windows

#### Opción 1: Chocolatey (Recomendado)
```bash
# Instalar Chocolatey si no lo tienes
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Redis
choco install redis-64

# Iniciar Redis
redis-server
```

#### Opción 2: WSL (Windows Subsystem for Linux)
```bash
# En WSL Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# Iniciar Redis
sudo service redis-server start

# Verificar que esté funcionando
redis-cli ping
```

#### Opción 3: Descarga Manual
1. Descargar Redis para Windows desde: https://github.com/microsoftarchive/redis/releases
2. Extraer el archivo ZIP
3. Ejecutar `redis-server.exe` desde la carpeta extraída

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server

# Iniciar Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verificar estado
sudo systemctl status redis-server
```

### macOS
```bash
# Usando Homebrew
brew install redis

# Iniciar Redis
brew services start redis

# O iniciar manualmente
redis-server
```

## 🔧 Configuración del Proyecto

### 1. Instalar dependencias Python
```bash
cd jwt_act2
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Configuración de la base de datos MariaDB
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=jwt_auth_db

# Configuración de Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Configuración JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=900
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Configuración de la aplicación
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Verificar conexiones
```bash
# Verificar MariaDB
mysql -u root -p -e "SELECT 1;"

# Verificar Redis
redis-cli ping
# Debería responder: PONG
```

### 4. Ejecutar la aplicación
```bash
python app.py
```

## 🧪 Pruebas

### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

Respuesta esperada:
```json
{
    "status": "healthy",
    "database": "connected",
    "redis": "connected",
    "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Prueba de rendimiento
```bash
python performance_test.py
```

### 3. Prueba manual con curl

#### Login SQL:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Login Redis:
```bash
curl -X POST http://localhost:5000/api-redis/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Comparación de rendimiento:
```bash
curl -X POST http://localhost:5000/api/performance/compare \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

## 🔍 Comandos Redis Útiles

### Conectar a Redis CLI
```bash
redis-cli
```

### Comandos básicos
```bash
# Ver todas las claves
KEYS *

# Ver claves de tokens revocados
KEYS revoked_token:*

# Ver claves de auditoría
KEYS audit_log:*

# Ver claves de sesiones
KEYS user_session:*

# Ver el valor de una clave específica
GET revoked_token:abc123

# Ver TTL de una clave
TTL revoked_token:abc123

# Limpiar todas las claves (¡CUIDADO!)
FLUSHALL

# Ver información del servidor
INFO

# Salir del CLI
EXIT
```

## 🐛 Troubleshooting

### Error: "Connection refused"
- Verificar que Redis esté ejecutándose: `redis-cli ping`
- Verificar el puerto en la configuración (por defecto 6379)
- Verificar que no haya firewall bloqueando la conexión

### Error: "ModuleNotFoundError: No module named 'redis'"
```bash
pip install redis==5.0.1
```

### Error: "Redis connection failed"
- Verificar que Redis esté iniciado
- Verificar configuración en `.env`
- Verificar que el host y puerto sean correctos

### Redis no inicia en Windows
- Verificar que el puerto 6379 no esté en uso
- Ejecutar como administrador
- Verificar logs de Redis

### WSL Redis no funciona
```bash
# En WSL
sudo service redis-server restart
sudo service redis-server status
```

## 📊 Monitoreo

### Ver estadísticas de Redis
```bash
redis-cli info stats
```

### Ver memoria usada
```bash
redis-cli info memory
```

### Ver claves por tipo
```bash
redis-cli info keyspace
```

## 🔒 Seguridad

### Configurar contraseña Redis
1. Editar `redis.conf`:
```
requirepass tu_contraseña_segura
```

2. Actualizar `.env`:
```env
REDIS_PASSWORD=tu_contraseña_segura
```

### Configurar Redis para producción
- Cambiar puerto por defecto
- Configurar bind a IP específica
- Habilitar autenticación
- Configurar límites de memoria
- Habilitar persistencia

## 📚 Recursos Adicionales

- [Documentación oficial de Redis](https://redis.io/documentation)
- [Redis Commands](https://redis.io/commands)
- [Redis Configuration](https://redis.io/topics/config)
- [Redis Security](https://redis.io/topics/security)
