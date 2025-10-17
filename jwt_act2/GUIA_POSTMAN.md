# 🚀 Guía para Probar la API con Postman

## 📋 Configuración Inicial

### 1. **Importar la Colección**
1. Abre Postman
2. Haz clic en **"Import"** (esquina superior izquierda)
3. Selecciona **"Upload Files"**
4. Importa el archivo: `postman_collection.json`

### 2. **Importar el Entorno**
1. En Postman, ve a **"Environments"** (esquina superior izquierda)
2. Haz clic en **"Import"**
3. Importa el archivo: `postman_environment.json`
4. Selecciona el entorno **"JWT Auth Environment"** en el dropdown

## 🧪 Pruebas Paso a Paso

### **Paso 1: Verificar Estado**
1. Selecciona **"Health Check"**
2. Haz clic en **"Send"**
3. **Resultado esperado:**
   ```json
   {
     "database": "connected",
     "status": "healthy",
     "timestamp": "2024-01-01T12:00:00"
   }
   ```

### **Paso 2: Registrar Usuario (Opcional)**
1. Selecciona **"Register User"**
2. Modifica los datos en el Body si quieres:
   ```json
   {
     "username": "mi_usuario",
     "email": "mi_email@example.com",
     "password": "mi_password"
   }
   ```
3. Haz clic en **"Send"**
4. **Resultado esperado:** Status 201 con datos del usuario

### **Paso 3: Login (Importante)**
1. Selecciona **"Login"**
2. Usa las credenciales por defecto:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
3. Haz clic en **"Send"**
4. **Resultado esperado:** Status 200 con tokens
5. **Los tokens se guardan automáticamente** en las variables de entorno

### **Paso 4: Probar Endpoints Autenticados**

#### **Ver Perfil:**
1. Selecciona **"Get Profile"**
2. Haz clic en **"Send"**
3. **Resultado esperado:** Status 200 con datos del usuario

#### **Ver Auditoría:**
1. Selecciona **"Get Audit Log"**
2. Haz clic en **"Send"**
3. **Resultado esperado:** Status 200 con historial de acciones

#### **Renovar Token:**
1. Selecciona **"Refresh Token"**
2. Haz clic en **"Send"**
3. **Resultado esperado:** Status 200 con nuevo access token

### **Paso 5: Logout**
1. Selecciona **"Logout"**
2. Haz clic en **"Send"**
3. **Resultado esperado:** Status 200 con mensaje de logout

## 🔧 Configuración Manual (Si no tienes los archivos)

### **Variables de Entorno:**
Crea un entorno con estas variables:
- `base_url`: `http://localhost:5000/api`
- `access_token`: (se llena automáticamente)
- `refresh_token`: (se llena automáticamente)

### **Headers por Defecto:**
Para requests POST, agrega:
- `Content-Type`: `application/json`

Para requests autenticados, agrega:
- `Authorization`: `Bearer {{access_token}}`

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/api/health` | Estado de la aplicación | No |
| POST | `/api/register` | Registrar usuario | No |
| POST | `/api/login` | Iniciar sesión | No |
| GET | `/api/profile` | Ver perfil | Sí |
| POST | `/api/refresh` | Renovar token | Refresh token |
| GET | `/api/audit-log` | Bitácora personal | Sí |
| GET | `/api/admin/audit-log` | Bitácora general | Sí |
| POST | `/api/logout` | Cerrar sesión | Sí |
| POST | `/api/logout-all` | Cerrar todas las sesiones | Sí |

## 🎯 Flujo de Pruebas Recomendado

1. **Health Check** → Verificar que la API esté funcionando
2. **Login** → Obtener tokens (se guardan automáticamente)
3. **Get Profile** → Verificar autenticación
4. **Get Audit Log** → Ver historial de acciones
5. **Refresh Token** → Probar renovación
6. **Logout** → Cerrar sesión

## 🐛 Troubleshooting

### **Error 401 (Unauthorized):**
- Verifica que hayas hecho login primero
- Revisa que el token esté en las variables de entorno
- El token puede haber expirado, haz refresh

### **Error 500 (Internal Server Error):**
- Verifica que la aplicación esté ejecutándose
- Revisa los logs de la aplicación
- Verifica la conexión a la base de datos

### **Error de Conexión:**
- Verifica que la aplicación esté en `http://localhost:5000`
- Revisa que no haya firewall bloqueando
- Verifica que el puerto 5000 esté libre

## 📝 Notas Importantes

- **Los tokens se guardan automáticamente** cuando haces login o refresh
- **El access token expira en 15 minutos** por defecto
- **El refresh token expira en 30 días** por defecto
- **Cada logout revoca el token actual**
- **Todas las acciones se registran en la auditoría**

## 🎉 ¡Listo!

Con esta configuración puedes probar completamente la API de autenticación JWT. Los tokens se manejan automáticamente, así que solo necesitas hacer login una vez y luego puedes probar todos los endpoints autenticados.
