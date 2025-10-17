#!/usr/bin/env python3
"""
Script simplificado para configurar la base de datos en Windows
"""

import mysql.connector
from mysql.connector import Error
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Configurar la base de datos y crear las tablas"""
    try:
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = connection.cursor()
        
        # Crear base de datos
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        logger.info(f"Base de datos {Config.DB_NAME} creada o ya existe")
        
        # Seleccionar la base de datos
        cursor.execute(f"USE {Config.DB_NAME}")
        
        # Crear tabla de usuarios
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(users_table)
        logger.info("Tabla 'users' creada o ya existe")
        
        # Crear tabla de tokens revocados
        revoked_tokens_table = """
        CREATE TABLE IF NOT EXISTS revoked_tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            jti VARCHAR(36) UNIQUE NOT NULL,
            token_type ENUM('access', 'refresh') NOT NULL,
            user_id INT NOT NULL,
            revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(revoked_tokens_table)
        logger.info("Tabla 'revoked_tokens' creada o ya existe")
        
        # Crear tabla de auditoría
        token_audit_table = """
        CREATE TABLE IF NOT EXISTS token_audit (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            action ENUM('login', 'logout', 'refresh', 'revoke') NOT NULL,
            token_jti VARCHAR(36),
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        cursor.execute(token_audit_table)
        logger.info("Tabla 'token_audit' creada o ya existe")
        
        # Crear índices para mejorar rendimiento
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_revoked_tokens_jti ON revoked_tokens(jti)",
            "CREATE INDEX IF NOT EXISTS idx_revoked_tokens_user_id ON revoked_tokens(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_token_audit_user_id ON token_audit(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_token_audit_created_at ON token_audit(created_at)"
        ]
        
        for index in indexes:
            cursor.execute(index)
        
        logger.info("Indices creados o ya existen")
        
        # Verificar tablas creadas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        logger.info(f"Tablas en la base de datos: {[table[0] for table in tables]}")
        
        cursor.close()
        connection.close()
        
        logger.info("Base de datos configurada exitosamente")
        return True
        
    except Error as e:
        logger.error(f"Error configurando base de datos: {e}")
        return False

def create_sample_user():
    """Crear un usuario de ejemplo"""
    try:
        from models import User
        
        # Conectar a la base de datos
        from database import db
        if not db.connect():
            logger.error("No se pudo conectar a la base de datos")
            return False
        
        # Verificar si ya existe un usuario de ejemplo
        existing_user = User.find_by_username("admin")
        if existing_user:
            logger.info("Usuario 'admin' ya existe")
            return True
        
        # Crear usuario de ejemplo
        password_hash = User.hash_password("admin123").decode('utf-8')
        user = User("admin", "admin@example.com", password_hash)
        
        if user.save():
            logger.info("Usuario 'admin' creado exitosamente (password: admin123)")
            return True
        else:
            logger.error("Error creando usuario de ejemplo")
            return False
            
    except Exception as e:
        logger.error(f"Error creando usuario de ejemplo: {e}")
        return False
    finally:
        db.disconnect()

def main():
    """Función principal"""
    print("Configurando base de datos MariaDB...")
    print(f"Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"Usuario: {Config.DB_USER}")
    print(f"Base de datos: {Config.DB_NAME}")
    print()
    
    # Configurar base de datos
    if setup_database():
        print("Base de datos configurada correctamente")
        
        # Crear usuario de ejemplo
        print("\nCreando usuario de ejemplo...")
        if create_sample_user():
            print("Usuario de ejemplo creado")
        else:
            print("Error creando usuario de ejemplo")
    else:
        print("Error configurando base de datos")
        print("\nVerifica que:")
        print("1. MariaDB esté ejecutándose")
        print("2. Las credenciales en config.py sean correctas")
        print("3. El usuario tenga permisos para crear bases de datos")

if __name__ == "__main__":
    main()
