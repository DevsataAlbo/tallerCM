import getpass
import psycopg2
import bcrypt

def validar_credenciales(conn, usuario, clave):
    with conn.cursor() as cursor:
        cursor.execute("SELECT clave FROM usuarios WHERE usuario = %s", (usuario,))
        registro = cursor.fetchone()
        if registro and bcrypt.checkpw(clave.encode('utf-8'), registro[0].encode('utf-8')):
            return True
        return False
