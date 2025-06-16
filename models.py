# models.py
from datetime import datetime, date

class Propietario:
    def __init__(self, nombre, telefono, direccion, id=None):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return (
            f"ID Propietario: {self.id}\n"
            f"Nombre: {self.nombre}\n"
            f"Teléfono: {self.telefono}\n"
            f"Dirección: {self.direccion}"
        )

class Mascota:
    def __init__(self, nombre, especie, raza, edad, propietario_id, id=None, propietario_nombre=None):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.propietario_id = propietario_id
        self.propietario_nombre = propietario_nombre

    def __str__(self):
        propietario_display = self.propietario_nombre if self.propietario_nombre else f"ID Propietario: {self.propietario_id}"
        return (
            f"ID Mascota: {self.id}\n"
            f"Nombre: {self.nombre}\n"
            f"Especie: {self.especie}\n"
            f"Raza: {self.raza}\n"
            f"Edad: {self.edad} años\n"
            f"Propietario: {propietario_display}"
        )

class Consulta:
    def __init__(self, fecha, motivo, diagnostico, mascota_id, id=None, mascota_nombre=None):
        self.id = id
        if isinstance(fecha, date):
            self.fecha = fecha
        elif isinstance(fecha, str):
            try:
                self.fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de fecha de la cadena incorrecto. Esperado YYYY-MM-DD.")
        else:
            raise ValueError("El argumento 'fecha' debe ser una cadena (YYYY-MM-DD) o un objeto datetime.date")
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota_id = mascota_id
        self.mascota_nombre = mascota_nombre

    def __str__(self):
        return (
            f"ID Consulta: {self.id}\n"
            f"Fecha: {self.fecha.strftime('%d-%m-%Y')}\n"
            f"Motivo: {self.motivo}\n"
            f"Diagnóstico: {self.diagnostico}\n"
            f"Mascota: {self.mascota_nombre if self.mascota_nombre else f'ID Mascota: {self.mascota_id}'}"
        )