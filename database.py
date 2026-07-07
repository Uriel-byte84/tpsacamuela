import sqlite3

def conectar_db():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect("saca_muela.db")

def inicializar_base_de_datos():
    """Crea las tablas necesarias si no existen en el sistema."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Creamos la tabla de pacientes basada en tu diseño UML
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        dni INTEGER PRIMARY KEY UNIQUE,
        nombre_apellido TEXT NOT NULL,
        telefono TEXT NOT NULL,
        email TEXT,
        obra_social TEXT NOT NULL,
        nro_afiliado TEXT,
        antecedentes_alergias TEXT
    )
    """)
    
    conexion.commit()
    conexion.close()

# --- OPERACIONES CRUD ---

def registrar_paciente(paciente_obj):
    """Recibe un objeto de la clase Paciente y lo guarda en la base de datos."""
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO pacientes VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            paciente_obj.dni, 
            paciente_obj.nombre_apellido, 
            paciente_obj.telefono, 
            paciente_obj.email,
            paciente_obj.obra_social, 
            paciente_obj.nro_afiliado, 
            paciente_obj.antecedentes_alergias
        ))
        conexion.commit()
        conexion.close()
        return True, "¡Paciente registrado con éxito!"
    except sqlite3.IntegrityError:
        return False, "Error: El DNI ya se encuentra registrado."

def obtener_pacientes():
    """Trae todos los registros de la tabla pacientes."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def borrar_paciente(dni):
    """Elimina un paciente del sistema mediante su DNI."""
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pacientes WHERE dni = ?", (dni,))
    conexion.commit()
    conexion.close()
