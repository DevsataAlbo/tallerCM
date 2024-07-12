import getpass
import psycopg2
import os
from db import conectar
from auth import validar_credenciales
from user_management import registrar_usuario, listar_usuarios
from centro_medico import ingresar_datos_centro_medico

def limpiar_pantalla():
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para Linux/MacOS
        os.system('clear')

def mostrar_menu_principal():
    print("\nMenu Principal")
    print("1. Registrar usuario")
    print("2. Listar usuarios registrados")
    print("3. Ingresar datos centro medico")
    print("4. Cerrar Sesión")
    return input("Selecciona una opción: ")

def main():
    conn = conectar()
    usuario = input("Usuario: ")
    clave = getpass.getpass("Clave: ")
    
    if validar_credenciales(conn, usuario, clave):
        while True:
            limpiar_pantalla()  # Limpiar la pantalla antes de mostrar el menú
            opcion = mostrar_menu_principal()
            limpiar_pantalla()  # Limpiar la pantalla antes de ejecutar la opción seleccionada
            if opcion == "1":
                registrar_usuario(conn)
            elif opcion == "2":
                listar_usuarios(conn)
            elif opcion == "3":
                ingresar_datos_centro_medico(conn)
            elif opcion == "4":
                print("Cerrando sesión...")
                break
            else:
                print("Opción inválida. Por favor, intenta de nuevo.")
    else:
        print("Credenciales incorrectas. Acceso denegado.")
    conn.close()

if __name__ == "__main__":
    main()
