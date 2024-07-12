import psycopg2
from psycopg2 import sql

def conectar():
    return psycopg2.connect(
        database="centro_medico",
        user="alumno",
        password="123456",
        host="localhost",
        port="5432"
    )

def crear_tablas(conn):
    comandos = (
        """
        CREATE TABLE IF NOT EXISTS nacionalidades (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS comunas (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS perfiles (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            rut VARCHAR(12) UNIQUE NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            sexo CHAR(1) NOT NULL,
            nacionalidad_id INTEGER NOT NULL REFERENCES nacionalidades(id),
            direccion VARCHAR(100) NOT NULL,
            comuna_id INTEGER NOT NULL REFERENCES comunas(id),
            telefono VARCHAR(15) NOT NULL,
            email VARCHAR(50) NOT NULL,
            perfil_id INTEGER NOT NULL REFERENCES perfiles(id),
            usuario VARCHAR(50) UNIQUE NOT NULL,
            clave VARCHAR(128) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS centro_medico_info (
            id SERIAL PRIMARY KEY,
            direccion VARCHAR(100),
            telefono VARCHAR(15),
            email VARCHAR(50),
            sitio_web VARCHAR(50)
        )
        """
    )
    
    with conn.cursor() as cursor:
        for comando in comandos:
            cursor.execute(comando)
        conn.commit()

def insertar_datos_iniciales(conn):
    datos = {
        'nacionalidades': [('Chilena',)],
        'comunas': [('Santiago',)],
        'perfiles': [('Admin',), ('Profesional medico',), ('Administrativo',), ('Paciente',)],
        'usuarios': [('Admin', 'User', '12345678-9', '1980-01-01', 'M', 1, 'Calle Falsa 123', 1, '123456789', 'admin@example.com', 1, 'admin', '$2b$12$D4G5f18o7aMMfwasBL7Gpu/90xwJ2i8fFv8C3cZ/PqV9mPYCBfQ1e')]
    }

    with conn.cursor() as cursor:
        for tabla, valores in datos.items():
            for valor in valores:
                if tabla == 'usuarios':
                    cursor.execute(sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier(tabla)), valor)
                else:
                    cursor.execute(sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s)").format(sql.Identifier(tabla)), valor)
        conn.commit()

if __name__ == "__main__":
    conn = conectar()
    crear_tablas(conn)
    insertar_datos_iniciales(conn)
    conn.close()
