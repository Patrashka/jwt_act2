# Guía Rápida de Instalación y Prueba

## ✅ Estado Actual

- ✅ **Redis**: Funcionando (simulador en memoria)
- ⚠️ **MariaDB**: Necesita instalación/configuración

## 🚀 Opciones para Ejecutar el Proyecto

### Opción 1: Solo Redis (Sin Base de Datos)

Puedes probar la funcionalidad Redis sin necesidad de MariaDB:

```bash
# Ejecutar la aplicación (ya está corriendo)
python app.py

# Probar health check
python test_redis_only.py
```

**Endpoints que funcionan sin BD:**
- ❌ `/api/login` - Requiere BD
- ❌ `/api-redis/login` - Requiere BD para buscar usuarios
- ✅ `/api/health` - Funciona (muestra estado de ambos servicios)

### Opción 2: Con MariaDB (Recomendado)

#### Instalación Rápida de MariaDB con Docker:

```bash
# Opción 1: Docker (más fácil)
docker run -d --name mariadb-jwt \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=jwt_auth_db \
  -p 3306:3306 \
  mariadb:10.6

# Verificar que está corriendo
docker ps
```

#### Instalación Manual de MariaDB:

```bash
# Con Chocolatey (como administrador)
choco install mariadb -y

# O descargar desde: https://mariadb.org/download/
```

**Después de instalar:**
```bash
# Iniciar MariaDB
net start mariadb

# O si es servicio con otro nombre
Get-Service | Where-Object {$_.Name -like "*mysql*" -or $_.Name -like "*maria*"}
```

### Opción 3: Usar Docker para Todo (Más Fácil)

```bash
# Iniciar Docker Desktop

# Ejecutar MariaDB
docker run -d --name mariadb-jwt \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=jwt_auth_db \
  -p 3306:3306 \
  mariadb:10.6

# Ejecutar Redis (opcional, el simulador ya funciona)
docker run -d --name redis-jwt \
  -p 6379:6379 \
  redis:7-alpine

# Verificar que están corriendo
docker ps

# Reiniciar la aplicación
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
  "timestamp": "2025-10-17T12:00:00"
}
```

### 2. Registro de Usuario (requiere BD)
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

### 3. Login SQL
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"password123\"}"
```

### 4. Login Redis
```bash
curl -X POST http://localhost:5000/api-redis/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"password123\"}"
```

### 5. Comparación de Rendimiento
```bash
curl -X POST http://localhost:5000/api/performance/compare \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"password123\"}"
```

## 📊 Pruebas de Rendimiento

```bash
# Script automatizado
python performance_test.py
```

## 🔧 Troubleshooting

### Redis muestra "usando simulador en memoria"
✅ **Esto es normal y está funcionando correctamente**. El simulador Redis en memoria funciona igual que Redis real para este proyecto.

### Database: "disconnected"
- Verificar que MariaDB esté corriendo
- Verificar credenciales en `config.py` o `.env`
- Usar Docker para MariaDB (más fácil)

### "Error 10061 connecting"
El servicio no está corriendo. Opciones:
1. Iniciar Docker Desktop y ejecutar contenedor
2. Iniciar servicio MariaDB: `net start mariadb`
3. Usar la versión sin BD (limitada)

## 📝 Configuración Actual

### Variables de Entorno
Crear archivo `.env` con:
```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=jwt_auth_db

# Redis (opcional, el simulador funciona sin esto)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

## 🎯 Resumen Rápido

**Para probar Redis ahora mismo (sin BD):**
```bash
python test_redis_only.py
```

**Para usar todo el proyecto:**
```bash
# 1. Iniciar Docker Desktop
# 2. Ejecutar MariaDB en Docker
docker run -d --name mariadb-jwt -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=jwt_auth_db -p 3306:3306 mariadb:10.6

# 3. Reiniciar aplicación
python app.py

# 4. Probar
python performance_test.py
```

## 🚀 Demo Rápida con Docker

```bash
# Script completo para ejecutar todo
# Copiar y pegar en PowerShell (como administrador):

# Detener contenedores existentes si los hay
docker stop mariadb-jwt 2>$null
docker rm mariadb-jwt 2>$null

# Iniciar MariaDB
docker run -d --name mariadb-jwt `
  -e MYSQL_ROOT_PASSWORD=password `
  -e MYSQL_DATABASE=jwt_auth_db `
  -p 3306:3306 `
  mariadb:10.6

# Esperar a que MariaDB inicie
Start-Sleep -Seconds 10

# La aplicación se reconectará automáticamente
Write-Host "✅ MariaDB iniciado en Docker"
Write-Host "🔄 Reinicia la aplicación: python app.py"
```
