class Persona:
    def __init__(self, dni, nombre_apellido, telefono, email):
        self.dni = dni
        self.nombre_apellido = nombre_apellido
        self.telefono = telefono
        self.email = email

class Paciente(Persona):
    def __init__(self, dni, nombre_apellido, telefono, email, obra_social, nro_afiliado, antecedentes_alergias):
        super().__init__(dni, nombre_apellido, telefono, email)
        self.obra_social = obra_social
        self.nro_afiliado = nro_afiliado
        self.antecedentes_alergias = antecedentes_alergias

class Odontologo(Persona):
    def __init__(self, dni, nombre_apellido, telefono, email, matricula, especialidad):
        super().__init__(dni, nombre_apellido, telefono, email)
        self.matricula = matricula
        self.especialidad = especialidad
