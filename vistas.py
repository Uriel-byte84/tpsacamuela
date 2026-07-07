import tkinter as tk
from tkinter import ttk, messagebox
import database
import modelos

class AppConsultorio:
    def __init__(self, root):
        self.root = root
        self.root.title("Consultorio Saca Muela - Panel de Control")
        self.root.geometry("750x500")
        
        # Inicializamos la base de datos por seguridad al abrir
        database.inicializar_base_de_datos()
        
        # Creamos el contenedor de pestañas (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestañas
        self.pestana_registro = ttk.Frame(self.notebook)
        self.pestana_tabla = ttk.Frame(self.notebook)
        
        self.notebook.add(self.pestana_registro, text="Registrar Paciente")
        self.notebook.add(self.pestana_tabla, text="Listado de Pacientes")
        
        # Construir el contenido de cada pestaña
        self.crear_interfaz_registro()
        self.crear_interfaz_tabla()

    def crear_interfaz_registro(self):
        # Contenedor con margen
        frame = ttk.LabelFrame(self.pestana_registro, text=" Datos Personales y Clínicos ")
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Etiquetas y Campos de texto
        campos = [
            ("DNI (Solo números):", "dni"),
            ("Nombre y Apellido:", "nombre"),
            ("Teléfono:", "tel"),
            ("Email:", "email"),
            ("Obra Social:", "os"),
            ("Nro Afiliado:", "nro"),
            ("Antecedentes / Alergias:", "alergias")
        ]
        
        self.variables = {}
        for idx, (txt, var_name) in enumerate(campos):
            ttk.Label(frame, text=txt, font=("Arial", 10)).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            self.variables[var_name] = ttk.Entry(frame, width=40)
            self.variables[var_name].grid(row=idx, column=1, padx=10, pady=5)
            
        # Botón de Registrar
        btn_registrar = ttk.Button(frame, text="Guardar Registro", command=self.guardar_paciente)
        btn_registrar.grid(row=len(campos), column=0, columnspan=2, pady=15)

    def guardar_paciente(self):
        # Capturamos los datos de los inputs
        try:
            dni = int(self.variables["dni"].get().strip())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un DNI numérico válido.")
            return
            
        nombre = self.variables["nombre"].get().strip()
        tel = self.variables["tel"].get().strip()
        email = self.variables["email"].get().strip()
        os = self.variables["os"].get().strip()
        nro = self.variables["nro"].get().strip()
        alergias = self.variables["alergias"].get().strip()
        
        if not nombre or not tel or not os:
            messagebox.showwarning("Atención", "Nombre, Teléfono y Obra Social son obligatorios.")
            return

        # Creamos el objeto Paciente mapeando tu diseño UML
        nuevo_paciente = modelos.Paciente(dni, nombre, tel, email, os, nro, allergies_placeholder := alergias)
        
        # Mandamos el objeto a la capa de base de datos
        exito, mensaje = database.registrar_paciente(nuevo_paciente)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            # Limpiamos los campos
            for entry in self.variables.values():
                entry.delete(0, tk.END)
            # Actualizamos la tabla automáticamente
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    def crear_interfaz_tabla(self):
        # Frame superior para acciones
        frame_acciones = ttk.Frame(self.pestana_tabla)
        frame_acciones.pack(fill="x", padx=15, pady=10)
        
        btn_actualizar = ttk.Button(frame_acciones, text="🔄 Actualizar Lista", command=self.actualizar_tabla)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_eliminar = ttk.Button(frame_acciones, text="❌ Borrar Seleccionado", command=self.eliminar_paciente)
        btn_eliminar.pack(side="right", padx=5)
        
        # Configuración de la Tabla (Treeview)
        columnas = ("DNI", "Nombre", "Teléfono", "Email", "Obra Social", "Nro Afiliado", "Alergias")
        self.tabla = ttk.Treeview(self.pestana_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")
            
        self.tabla.pack(fill="both", expand=True, padx=15, pady=10)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        # Limpiar filas previas
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
            
        # Traer registros desde la base de datos
        lista_pacientes = database.obtener_pacientes()
        for p in lista_pacientes:
            self.tabla.insert("", "end", values=p)

    def eliminar_paciente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona un paciente de la lista.")
            return
            
        valores = self.tabla.item(seleccion[0])["values"]
        dni_paciente = valores[0]
        nombre_paciente = valores[1]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar a {nombre_paciente}?")
        if confirmar:
            database.borrar_paciente(dni_paciente)
            messagebox.showinfo("Eliminado", "El registro ha sido removido.")
            self.actualizar_tabla()
