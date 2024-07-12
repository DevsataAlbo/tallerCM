import psycopg2

def ingresar_datos_centro_medico(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM centro_medico_info WHERE id = 1")
        centro_medico = cursor.fetchone()
    
    if centro_medico:
        print("\nDatos del Centro Medico")
        print(f"Dirección: {centro_medico[1]}")
        print(f"Teléfono: {centro_medico[2]}")
        print(f"Email: {centro_medico[3]}")
        print(f"Sitio web: {centro_medico[4]}")
        
        print("\n1. Editar información")
        print("2. Volver al menu anterior")
        
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            editar_datos_centro_medico(conn)
    else:
        print("No se encontraron datos del centro medico.")
        print("1. Ingresar nueva información")
        print("2. Volver al menu anterior")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            editar_datos_centro_medico(conn)

def editar_datos_centro_medico(conn):
    print("\nEditar Datos del Centro Medico")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    sitio_web = input("Sitio web: ")
    
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO centro_medico_info (id, direccion, telefono, email, sitio_web)
            VALUES (1, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE 
            SET direccion = EXCLUDED.direccion,
                telefono = EXCLUDED.telefono,
                email = EXCLUDED.email,
                sitio_web = EXCLUDED.sitio_web
        """, (direccion, telefono, email, sitio_web))
        conn.commit()
    print("Información del centro medico actualizada exitosamente.")
