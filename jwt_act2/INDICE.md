# 📚 Índice de Documentación - JWT Act2

## 🚀 Inicio Rápido
Para comenzar rápidamente, lee estos archivos en orden:

1. **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** - Visión general del proyecto y resultados
2. **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Instalación y prueba rápida
3. **[README.md](README.md)** - Documentación completa

## 📖 Documentación Completa

### Documentos Principales

| Archivo | Descripción | Para quién |
|---------|-------------|------------|
| **[README.md](README.md)** | Documentación completa del proyecto | Todos |
| **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** | Resumen del proyecto, arquitectura y resultados | Evaluadores, gerentes |
| **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** | Inicio rápido con Docker | Desarrolladores nuevos |

### Guías de Instalación

| Archivo | Descripción | Para quién |
|---------|-------------|------------|
| **[INSTALACION_REDIS.md](INSTALACION_REDIS.md)** | Instalación detallada de Redis | Desarrolladores, DevOps |
| **[COMANDOS_UTILES.md](COMANDOS_UTILES.md)** | Comandos útiles para desarrollo | Desarrolladores |

### Testing y API

| Archivo | Descripción | Para quién |
|---------|-------------|------------|
| **[GUIA_POSTMAN.md](GUIA_POSTMAN.md)** | Guía para usar Postman | Testers, desarrolladores |
| **[postman_collection.json](postman_collection.json)** | Colección de Postman | Testers |
| **[postman_environment.json](postman_environment.json)** | Variables de entorno | Testers |

## 💻 Archivos de Código

### Core Application

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| **[app.py](app.py)** | Aplicación Flask principal con todos los endpoints | ~790 |
| **[config.py](config.py)** | Configuración centralizada (DB, Redis, JWT) | ~30 |
| **[models.py](models.py)** | Modelos de datos (User, Token, Audit) | ~200 |
| **[database.py](database.py)** | Gestor de conexión MariaDB | ~156 |

### Redis Integration

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| **[redis_manager.py](redis_manager.py)** | Gestor de Redis con fallback automático | ~230 |
| **[redis_alternative.py](redis_alternative.py)** | Simulador Redis en memoria | ~155 |

### Testing

| Archivo | Descripción | Líneas |
|---------|-------------|--------|
| **[performance_test.py](performance_test.py)** | Script de pruebas de rendimiento | ~180 |

### Setup

| Archivo | Descripción | Plataforma |
|---------|-------------|------------|
| **[setup_windows.py](setup_windows.py)** | Script de configuración | Windows |
| **[start_windows.bat](start_windows.bat)** | Script de inicio | Windows |
| **[requirements.txt](requirements.txt)** | Dependencias Python | Todas |

## 🎯 Por Caso de Uso

### "Quiero instalar y ejecutar el proyecto"
1. [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Instalación rápida con Docker
2. [README.md](README.md) - Instalación detallada

### "Quiero entender qué hace el proyecto"
1. [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - Resumen ejecutivo
2. [README.md](README.md) - Documentación completa

### "Quiero probar la API"
1. [GUIA_POSTMAN.md](GUIA_POSTMAN.md) - Guía de Postman
2. [postman_collection.json](postman_collection.json) - Importar colección
3. [COMANDOS_UTILES.md](COMANDOS_UTILES.md) - Ejemplos con curl

### "Quiero comparar SQL vs Redis"
1. Ejecutar: `python performance_test.py`
2. O usar: `POST /api/performance/compare`
3. Ver [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - Sección de resultados

### "Redis no funciona"
1. [INSTALACION_REDIS.md](INSTALACION_REDIS.md) - Instalación de Redis
2. [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Usar Docker para Redis
3. **Nota**: El simulador en memoria se activa automáticamente

### "Necesito comandos para desarrollo"
1. [COMANDOS_UTILES.md](COMANDOS_UTILES.md) - Todos los comandos útiles

### "Tengo problemas"
1. [COMANDOS_UTILES.md](COMANDOS_UTILES.md) - Sección Troubleshooting
2. [README.md](README.md) - Sección Troubleshooting

## 📊 Estructura del Proyecto

```
jwt_act2/
│
├── 📄 Documentación
│   ├── README.md                    # Documentación principal
│   ├── RESUMEN_EJECUTIVO.md         # Resumen del proyecto
│   ├── GUIA_RAPIDA.md              # Guía de inicio rápido
│   ├── INSTALACION_REDIS.md        # Instalación de Redis
│   ├── COMANDOS_UTILES.md          # Comandos útiles
│   ├── GUIA_POSTMAN.md             # Guía de Postman
│   └── INDICE.md                   # Este archivo
│
├── 🐍 Código Python
│   ├── app.py                      # Aplicación Flask
│   ├── config.py                   # Configuración
│   ├── database.py                 # Gestor MariaDB
│   ├── models.py                   # Modelos de datos
│   ├── redis_manager.py            # Gestor Redis
│   └── redis_alternative.py        # Simulador Redis
│
├── 🧪 Testing
│   ├── performance_test.py         # Pruebas de rendimiento
│   ├── postman_collection.json     # Colección Postman
│   └── postman_environment.json    # Variables Postman
│
├── ⚙️ Configuración
│   ├── requirements.txt            # Dependencias
│   ├── setup_windows.py            # Setup Windows
│   ├── start_windows.bat           # Inicio Windows
│   └── .gitignore                  # Git ignore
│
└── 📁 Runtime
    └── __pycache__/                # Cache Python (auto)
```

## 🔑 Endpoints Principales

### SQL (Originales)
- `POST /api/register` - Registro
- `POST /api/login` - Login SQL
- `POST /api/logout` - Logout SQL
- `GET /api/profile` - Perfil
- `GET /api/audit-log` - Auditoría SQL

### Redis (Nuevos)
- `POST /api-redis/login` - Login Redis
- `POST /api-redis/logout` - Logout Redis
- `GET /api-redis/audit-log` - Auditoría Redis

### Utilidades
- `GET /api/health` - Estado del sistema
- `POST /api/performance/compare` - Comparación SQL vs Redis

## 📞 Soporte

### Información del Proyecto
- **Versión**: 2.0 (Act2)
- **Framework**: Flask 2.3.3
- **Python**: 3.7+
- **Bases de datos**: MariaDB 10.6, Redis 7

### Recursos Externos
- [Documentación Flask](https://flask.palletsprojects.com/)
- [Documentación JWT](https://flask-jwt-extended.readthedocs.io/)
- [Documentación Redis](https://redis.io/documentation)
- [Documentación MariaDB](https://mariadb.com/kb/en/)

## ✅ Checklist de Evaluación

Para evaluadores, verificar que existan:

- [x] README.md completo
- [x] RESUMEN_EJECUTIVO.md
- [x] Código fuente completo y funcional
- [x] Endpoints SQL implementados
- [x] Endpoints Redis implementados
- [x] Endpoint de comparación
- [x] Medición de tiempos
- [x] Simulador Redis como fallback
- [x] Documentación de API
- [x] Colección de Postman
- [x] Script de pruebas
- [x] Instrucciones de instalación
- [x] requirements.txt
- [x] Docker compose/comandos

## 🎓 Notas de Entrega

Este proyecto demuestra:
1. Integración de Redis como cache
2. Comparación de rendimiento SQL vs Redis
3. Implementación de arquitectura híbrida
4. Fallback automático ante fallas
5. Medición precisa de rendimiento
6. Documentación completa

**Total de líneas de código**: ~1,800 líneas
**Total de documentación**: ~2,500 líneas
**Total de archivos**: 18 archivos

---

📅 **Fecha**: Octubre 2025  
👨‍💻 **Proyecto**: JWT Authentication System - Act2


