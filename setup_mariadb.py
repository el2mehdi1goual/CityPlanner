#!/usr/bin/env python
"""
Script pour créer la base de données MariaDB pour le projet Django
"""
import pymysql
import sys

# Configuration MariaDB
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'mehdi'
DB_NAME = 'ai_urban_design'
DB_CHARSET = 'utf8mb4'

try:
    # Connexion au serveur MySQL/MariaDB
    print(f"Tentative de connexion à MariaDB sur {DB_HOST}...")
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )
    
    cursor = conn.cursor()
    
    # Créer la base de données
    print(f"Création de la base de données '{DB_NAME}'...")
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.execute(f"""
        CREATE DATABASE {DB_NAME} 
        CHARACTER SET {DB_CHARSET} 
        COLLATE utf8mb4_unicode_ci
    """)
    print(f"✓ Base de données '{DB_NAME}' créée avec succès")
    
    cursor.close()
    conn.close()
    
except pymysql.err.OperationalError as e:
    print(f"✗ Erreur de connexion: {e}")
    print("\nAssurez-vous que:")
    print("  1. MariaDB/MySQL est installé et en cours d'exécution")
    print("  2. Le serveur écoute sur localhost:3306")
    print("  3. L'utilisateur 'root' existe")
    sys.exit(1)
except Exception as e:
    print(f"✗ Erreur: {e}")
    sys.exit(1)
