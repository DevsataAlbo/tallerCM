import psycopg2
import bcrypt
from tabulate import tabulate
from datetime import datetime

def registrar_usuario(conn):
    print("\nRegistrar Usuario")
    print("Ingresa el numero del perfil que quieres ingresar:")
    print("1. Profesional medico")
    print("2. Administrativo")
    print("3. Paciente")
    print("4. Volver al menu anterior")
    perfil_opcion = input("Selecciona una opción: ")
    
    perfiles = {"1": 2, "2": 3, "3": 4}  # IDs de perfiles en la base de datos
    perfil_id = perfiles.get(perfil_opcion)
    
    if not perfil_id:
        return
    
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    rut = input("RUT: ")
    fecha_nacimiento = input("Fecha de nacimiento (DD-MM-AAAA): ")
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("Formato de fecha inválido. Debe ser DD-MM-AAAA.")
        return

    sexo = input("Sexo (M/F): ")
    nacionalidad_id = input("ID de Nacionalidad: ")
    print("1 - Santiago ; 2 - Puente Alto")
    comuna_id = input("ID de Comuna: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    usuario = input("Nombre de usuario: ")
    clave = bcrypt.hashpw(input("Clave: ").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, rut, fecha_nacimiento, sexo, nacionalidad_id, direccion, comuna_id, telefono, email, perfil_id, usuario, clave)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, rut, fecha_nacimiento, sexo, nacionalidad_id, direccion, comuna_id, telefono, email, perfil_id, usuario, clave))
        conn.commit()
    print("Usuario registrado exitosamente.")

def listar_usuarios(conn):
    print("\nListar Usuarios Registrados")
    print("Ingresa el numero del perfil que quieres listar:")
    print("1. Profesional medico")
    print("2. Administrativo")
    print("3. Paciente")
    print("4. Todos")
    print("5. Volver al menu anterior")
    perfil_opcion = input("Selecciona una opción: ")

    perfiles = {"1": 2, "2": 3, "3": 4}
    perfil_id = perfiles.get(perfil_opcion)
    
    query = """
    SELECT u.id, u.nombre, u.apellido, u.rut, p.nombre as perfil
    FROM usuarios u
    JOIN perfiles p ON u.perfil_id = p.id
    """
    
    if perfil_id:
        query += f" WHERE perfil_id = {perfil_id}"
    
    with conn.cursor() as cursor:
        cursor.execute(query)
        usuarios = cursor.fetchall()
    
    if not usuarios:
        print("No se encontraron usuarios.")
        return
    
    headers = ["ID", "Nombre", "Apellido", "RUT", "Perfil"]
    print(tabulate(usuarios, headers, tablefmt="grid"))
    
    usuario_id = input("Ingresa el numero del usuario que quieres ver o 'q' para volver al menu anterior: ")
    if usuario_id.lower() == 'q':
        return
    
    with conn.cursor() as cursor:
        cursor.execute("""
        SELECT u.nombre, u.apellido, u.rut, p.nombre as perfil, u.fecha_nacimiento, u.sexo, n.nombre as nacionalidad, u.direccion, c.nombre as comuna, u.telefono, u.email
        FROM usuarios u
        JOIN perfiles p ON u.perfil_id = p.id
        JOIN nacionalidades n ON u.nacionalidad_id = n.id
        JOIN comunas c ON u.comuna_id = c.id
        WHERE u.id = %s
        """, (usuario_id,))
        usuario = cursor.fetchone()
    
    if usuario:
        print(f"\nNombre: {usuario[0]}")
        print(f"Apellido: {usuario[1]}")
        print(f"RUT: {usuario[2]}")
        print(f"Perfil: {usuario[3]}")
        print(f"Fecha de nacimiento: {usuario[4]}")
        print(f"Sexo: {usuario[5]}")
        print(f"Nacionalidad: {usuario[6]}")
        print(f"Dirección: {usuario[7]}")
        print(f"Comuna: {usuario[8]}")
        print(f"Teléfono: {usuario[9]}")
        print(f"Email: {usuario[10]}")
        
        print("\n1. Editar usuario")
        print("2. Eliminar usuario")
        print("3. Volver al menu anterior")
        
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            editar_usuario(conn, usuario_id)
        elif opcion == "2":
            eliminar_usuario(conn, usuario_id)

def editar_usuario(conn, usuario_id):
    print("\nEditar Usuario")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    rut = input("RUT: ")
    fecha_nacimiento = input("Fecha de nacimiento (DD-MM-AAAA): ")
    sexo = input("Sexo (M/F): ")
    nacionalidad_id = input("ID de Nacionalidad: ")
    print("1 - Santiago ; 2 - Puente Alto")
    comuna_id = input("ID de Comuna: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    clave = bcrypt.hashpw(input("Clave: ").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE usuarios SET
            nombre = %s, apellido = %s, rut = %s, fecha_nacimiento = %s, sexo = %s,
            nacionalidad_id = %s, direccion = %s, comuna_id = %s, telefono = %s, email = %s, clave = %s
            WHERE id = %s
        """, (nombre, apellido, rut, fecha_nacimiento, sexo, nacionalidad_id, direccion, comuna_id, telefono, email, clave, usuario_id))
        conn.commit()
    print("Usuario actualizado exitosamente.")

def eliminar_usuario(conn, usuario_id):
    confirmacion = input("¿Estás seguro de que quieres eliminar este usuario? (s/n): ")
    if confirmacion.lower() == 's':
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            conn.commit()
        print("Usuario eliminado exitosamente.")
