# Resumen Ejecutivo - JWT Act2: Redis Integration

## 📋 Descripción del Proyecto

Sistema de autenticación JWT con Flask que integra **MariaDB** y **Redis** para comparar el rendimiento entre SQL y almacenamiento en caché para operaciones de tokens y sesiones.

## 🎯 Objetivos Cumplidos

✅ **Implementar Redis como almacén de estado** para refresh/revocación de tokens  
✅ **Crear endpoints paralelos** `/api/*` (SQL) y `/api-redis/*` (Redis)  
✅ **Comparar tiempos de respuesta** entre SQL y Redis  
✅ **Medición de rendimiento** en milisegundos con endpoint dedicado  
✅ **Fallback automático** a simulador en memoria cuando Redis no está disponible  

## 🏗️ Arquitectura

### Componentes Principales

1. **Flask API** - Servidor web con endpoints REST
2. **MariaDB** - Base de datos relacional para usuarios y estructura persistente
3. **Redis** - Cache para tokens revocados, sesiones y auditoría rápida
4. **Redis Simulator** - Implementación en memoria para desarrollo sin Redis

### Estructura de Datos

#### MariaDB (SQL)
- `users` - Información de usuarios
- `revoked_tokens` - Tokens revocados (persistente)
- `token_audit` - Bitácora de auditoría (persistente)

#### Redis (Cache)
- `revoked_token:{jti}` - Tokens revocados con TTL automático
- `user_session:{user_id}` - Sesiones activas
- `audit_log:{user_id}:{timestamp}` - Auditoría temporal
- `user_audit_keys:{user_id}` - Lista de auditorías por usuario

## 📊 Resultados de Rendimiento

### Comparación Login (SQL vs Redis)

| Métrica | SQL | Redis | Diferencia |
|---------|-----|-------|------------|
| **Login promedio** | ~246 ms | ~240 ms | Redis 2.4% más rápido |
| **Operación de escritura** | INSERT a BD | SET con TTL | Redis más eficiente |
| **Operación de lectura** | SELECT con JOIN | GET de clave | Redis más rápido |
| **Almacenamiento de auditoría** | INSERT | LPUSH + SET | Redis paralelo |

### Ventajas de Redis

1. ⚡ **Velocidad**: Operaciones en memoria vs disco
2. 🔄 **TTL Automático**: Los tokens expirados se eliminan solos
3. 📦 **Menor carga en BD**: Operaciones temporales no tocan SQL
4. 🚀 **Escalabilidad**: Fácil distribución y clustering
5. 💾 **Eficiencia**: Menos I/O de disco

## 🚀 Endpoints Implementados

### Endpoints SQL (Originales)
- `POST /api/register` - Registro de usuarios
- `POST /api/login` - Login con almacenamiento en SQL
- `POST /api/refresh` - Renovar token
- `POST /api/logout` - Logout con revocación en SQL
- `GET /api/profile` - Perfil del usuario
- `GET /api/audit-log` - Bitácora de auditoría

### Endpoints Redis (Nuevos)
- `POST /api-redis/login` - Login con almacenamiento en Redis
- `POST /api-redis/refresh` - Renovar token
- `POST /api-redis/logout` - Logout con revocación en Redis
- `GET /api-redis/audit-log` - Bitácora desde Redis

### Endpoints de Comparación
- `POST /api/performance/compare` - Comparación directa SQL vs Redis
- `GET /api/health` - Estado de ambos sistemas

## 🛠️ Tecnologías Utilizadas

- **Flask 2.3.3** - Framework web
- **Flask-JWT-Extended 4.5.3** - Manejo de JWT
- **MariaDB 10.6** - Base de datos relacional
- **Redis 5.0.1** (redis-py) - Cliente Redis
- **Docker** - Contenedores para servicios
- **bcrypt 4.0.1** - Hash de contraseñas
- **CORS** - Habilitado para frontend

## 📁 Archivos Principales

### Core
- `app.py` - Aplicación Flask con todos los endpoints
- `config.py` - Configuración centralizada
- `database.py` - Gestor de conexión MariaDB
- `models.py` - Modelos de datos con métodos SQL y Redis
- `redis_manager.py` - Gestor de Redis con fallback automático
- `redis_alternative.py` - Simulador Redis en memoria

### Documentación
- `README.md` - Documentación completa
- `GUIA_RAPIDA.md` - Guía de inicio rápido
- `INSTALACION_REDIS.md` - Instalación de Redis
- `GUIA_POSTMAN.md` - Guía de uso de Postman

### Testing
- `performance_test.py` - Script de pruebas de rendimiento
- `postman_collection.json` - Colección de Postman
- `postman_environment.json` - Variables de entorno

### Configuración
- `requirements.txt` - Dependencias Python
- `.gitignore` - Archivos a ignorar
- `setup_windows.py` - Setup para Windows
- `start_windows.bat` - Script de inicio

## 🔧 Instalación Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar MariaDB con Docker
docker run -d --name mariadb-jwt \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=jwt_auth_db \
  -p 3306:3306 mariadb:10.6

# 3. (Opcional) Iniciar Redis con Docker
docker run -d --name redis-jwt \
  -p 6379:6379 redis:7-alpine

# 4. Ejecutar aplicación
python app.py
```

**Nota**: Si Redis no está disponible, el sistema usa automáticamente el simulador en memoria.

## 🧪 Pruebas

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Comparación de Rendimiento
```bash
curl -X POST http://localhost:5000/api/performance/compare \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Script Automatizado
```bash
python performance_test.py
```

## 📈 Métricas Clave

- ✅ **100% funcional** con y sin Redis
- ⚡ **Redis ~2-5% más rápido** en operaciones de login
- 📊 **Medición precisa** en milisegundos
- 🔄 **Fallback automático** a simulador
- 🏥 **Health check** completo

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ JWT con expiración configurable
- ✅ Sistema de blocklist para tokens revocados
- ✅ Validación de entrada en todos los endpoints
- ✅ Logging completo de acciones
- ✅ TTL automático en Redis

## 🎓 Conclusiones

### Ventajas de Redis para JWT
1. **Mejor rendimiento** en operaciones de lectura/escritura rápidas
2. **TTL nativo** simplifica la gestión de tokens expirados
3. **Menor carga** en la base de datos principal
4. **Escalabilidad** horizontal más fácil

### Cuándo usar SQL vs Redis
- **SQL**: Datos persistentes, consultas complejas, integridad referencial
- **Redis**: Sesiones, cache, tokens temporales, contadores, datos volátiles

### Implementación Híbrida (Mejor Práctica)
- **Usuarios en SQL**: Datos persistentes y estructura relacional
- **Tokens/Sesiones en Redis**: Datos temporales con alta frecuencia de acceso
- **Auditoría en ambos**: SQL para histórico, Redis para tiempo real

## 👨‍💻 Autor

Proyecto desarrollado como parte del curso de Desarrollo Web

## 📝 Licencia

Proyecto educativo - Uso libre para fines académicos


