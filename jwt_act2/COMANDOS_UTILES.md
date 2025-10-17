# Comandos Útiles - JWT Act2

## 🐳 Docker

### Gestión de Contenedores

```bash
# Ver contenedores en ejecución
docker ps

# Detener contenedores
docker stop mariadb-jwt redis-jwt

# Iniciar contenedores existentes
docker start mariadb-jwt redis-jwt

# Eliminar contenedores
docker rm -f mariadb-jwt redis-jwt

# Ver logs de contenedores
docker logs mariadb-jwt
docker logs redis-jwt

# Ver logs en tiempo real
docker logs -f mariadb-jwt
```

### Reinicio Completo

```bash
# Detener y eliminar todo
docker stop mariadb-jwt redis-jwt
docker rm mariadb-jwt redis-jwt

# Crear nuevamente
docker run -d --name mariadb-jwt -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=jwt_auth_db -p 3306:3306 mariadb:10.6
docker run -d --name redis-jwt -p 6379:6379 redis:7-alpine
```

## 🧪 Pruebas con curl

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Registro de Usuario
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

### Login SQL
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Login Redis
```bash
curl -X POST http://localhost:5000/api-redis/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Comparación de Rendimiento
```bash
curl -X POST http://localhost:5000/api/performance/compare \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

### Obtener Perfil (con token)
```bash
# Guardar token del login
TOKEN="tu_access_token_aqui"

curl http://localhost:5000/api/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Logout
```bash
curl -X POST http://localhost:5000/api/logout \
  -H "Authorization: Bearer $TOKEN"
```

## 🔍 PowerShell (Windows)

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get
```

### Login SQL
```powershell
$body = @{username="admin"; password="admin123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/login" -Method POST -Body $body -ContentType "application/json"
```

### Login Redis
```powershell
$body = @{username="admin"; password="admin123"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api-redis/login" -Method POST -Body $body -ContentType "application/json"
```

### Comparación
```powershell
$body = @{username="admin"; password="admin123"} | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:5000/api/performance/compare" -Method POST -Body $body -ContentType "application/json"
$result.performance_analysis | ConvertTo-Json
```

## 🐍 Python

### Script de Pruebas
```bash
python performance_test.py
```

### Iniciar Aplicación
```bash
python app.py
```

### Detener Aplicación
```bash
# Ctrl+C en la terminal
# O en otra terminal:
taskkill /F /IM python.exe  # Windows
pkill -f "python app.py"     # Linux/Mac
```

## 🗄️ MariaDB

### Conectar a la Base de Datos
```bash
# Conectar al contenedor
docker exec -it mariadb-jwt mysql -uroot -ppassword jwt_auth_db

# Ver tablas
SHOW TABLES;

# Ver usuarios
SELECT * FROM users;

# Ver tokens revocados
SELECT * FROM revoked_tokens;

# Ver auditoría
SELECT * FROM token_audit ORDER BY created_at DESC LIMIT 10;
```

### Respaldo y Restauración
```bash
# Hacer respaldo
docker exec mariadb-jwt mysqldump -uroot -ppassword jwt_auth_db > backup.sql

# Restaurar respaldo
docker exec -i mariadb-jwt mysql -uroot -ppassword jwt_auth_db < backup.sql
```

## 🔴 Redis CLI

### Conectar a Redis (si está corriendo)
```bash
# Conectar al contenedor
docker exec -it redis-jwt redis-cli

# Ver todas las claves
KEYS *

# Ver tokens revocados
KEYS revoked_token:*

# Ver sesiones
KEYS user_session:*

# Ver auditoría
KEYS audit_log:*

# Ver valor de una clave
GET revoked_token:abc123

# Ver TTL de una clave
TTL revoked_token:abc123

# Limpiar todo (¡CUIDADO!)
FLUSHALL

# Ver estadísticas
INFO stats

# Salir
EXIT
```

## 📊 Monitoreo

### Ver Procesos Python
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

### Ver Uso de Puertos
```bash
# Windows
netstat -ano | findstr :5000
netstat -ano | findstr :3306
netstat -ano | findstr :6379

# Linux/Mac
lsof -i :5000
lsof -i :3306
lsof -i :6379
```

### Ver Logs de la Aplicación
```bash
# Si usas el script start_windows.bat, los logs están en la consola
# Para guardar logs:
python app.py > app.log 2>&1
```

## 🧹 Limpieza

### Limpiar Python
```bash
# Eliminar cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Windows PowerShell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force
```

### Limpiar Docker
```bash
# Detener y eliminar contenedores
docker stop mariadb-jwt redis-jwt
docker rm mariadb-jwt redis-jwt

# Eliminar volúmenes huérfanos
docker volume prune -f

# Eliminar imágenes no usadas
docker image prune -a -f
```

## 🔧 Troubleshooting

### Puerto ya en uso
```bash
# Windows - Encontrar proceso usando puerto 5000
netstat -ano | findstr :5000
# Matar proceso (reemplazar PID)
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Reiniciar todo desde cero
```bash
# 1. Detener aplicación (Ctrl+C)
# 2. Detener y eliminar contenedores
docker stop mariadb-jwt redis-jwt
docker rm mariadb-jwt redis-jwt

# 3. Eliminar cache Python
# Windows
Remove-Item -Path __pycache__ -Recurse -Force

# 4. Reiniciar contenedores
docker run -d --name mariadb-jwt -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=jwt_auth_db -p 3306:3306 mariadb:10.6
docker run -d --name redis-jwt -p 6379:6379 redis:7-alpine

# 5. Esperar 10 segundos
Start-Sleep -Seconds 10

# 6. Iniciar aplicación
python app.py
```

## 📝 Notas

- El simulador Redis se activa automáticamente si Redis no está disponible
- Los tokens tienen TTL automático en Redis
- MariaDB requiere ~10 segundos para iniciar completamente
- Todos los endpoints retornan tiempos de respuesta en milisegundos


