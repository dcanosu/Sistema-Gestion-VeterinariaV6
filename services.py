# services.py
import logging
from datetime import datetime
from models import Propietario, Mascota, Consulta
from database import DatabaseManager
from ui import UIUtils

class SistemaVeterinaria:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def _get_propietario_or_create(self, owner_name):
        propietario = self.db_manager.get_propietario_by_nombre(owner_name)
        if not propietario:
            UIUtils.print_message(f"El propietario '{owner_name}' no está registrado.")
            if UIUtils.confirm_action("¿Desea registrarlo ahora?"):
                nombre = input("Nombre del NUEVO dueño: ").strip()
                propietario_existente = self.db_manager.get_propietario_by_nombre(nombre)
                if propietario_existente:
                    print(f"El propietario '{nombre}' ya existe. Asignando mascota a este propietario.")
                    return propietario_existente
                telefono = input("Teléfono del NUEVO dueño: ")
                direccion = input("Dirección del NUEVO dueño: ")
                propietario = Propietario(nombre, telefono, direccion)
                propietario_registrado = self.db_manager.insert_propietario(propietario)
                if propietario_registrado:
                    print("Dueño registrado con éxito.")
                    logging.info(f"Dueño: {propietario_registrado.nombre} (ID: {propietario_registrado.id}) registrado.")
                return propietario_registrado
            else:
                UIUtils.print_message("Operación cancelada. Propietario no encontrado ni registrado.")
                logging.info("Registro de mascota/operación cancelada: propietario no encontrado/registrado.")
                return None
        return propietario

    def _get_mascota(self, prompt="Ingrese el ID de la mascota: "):
        mascota_id = UIUtils.get_int_input(prompt, "ID de mascota inválido.")
        mascota = self.db_manager.get_mascota_by_id(mascota_id)
        if not mascota:
            UIUtils.print_message(f"No se encontró ninguna mascota con el ID: {mascota_id}.")
            logging.info(f"Mascota con ID {mascota_id} no encontrada.")
        return mascota

    def _get_propietario(self, prompt="Ingrese el ID del propietario: "):
        propietario_id = UIUtils.get_int_input(prompt, "ID de propietario inválido.")
        propietario = self.db_manager.get_propietario_by_id(propietario_id)
        if not propietario:
            UIUtils.print_message(f"No se encontró ningún propietario con el ID: {propietario_id}.")
            logging.info(f"Propietario con ID {propietario_id} no encontrado.")
        return propietario

    def _get_consulta(self, prompt="Ingrese el ID de la consulta: "):
        consulta_id = UIUtils.get_int_input(prompt, "ID de consulta inválido.")
        consulta = self.db_manager.get_consulta_by_id(consulta_id)
        if not consulta:
            UIUtils.print_message(f"No se encontró ninguna consulta con el ID: {consulta_id}.")
            logging.info(f"Consulta con ID {consulta_id} no encontrada.")
        return consulta

    def registrar_mascota(self):
        UIUtils.print_title("Registrar Mascota")
        nombre_mascota = input("Nombre de la mascota: ")
        especie_mascota = input("Especie de la mascota: ")
        raza_mascota = input("Raza de la mascota: ")
        edad_mascota = UIUtils.get_int_input("Edad de la mascota en años: ")
        while edad_mascota < 0:
            print("La edad no puede ser negativa.")
            edad_mascota = UIUtils.get_int_input("Edad de la mascota en años: ")

        UIUtils.print_message("--- Información del Propietario ---")
        nombre_propietario = input("Ingrese el nombre del dueño existente o nuevo: ").strip()
        propietario = self._get_propietario_or_create(nombre_propietario)

        if not propietario:
            return

        mascota = Mascota(nombre_mascota, especie_mascota, raza_mascota, edad_mascota, propietario.id)
        mascota_registrada = self.db_manager.insert_mascota(mascota)
        if mascota_registrada:
            print(f"\n - Mascota '{mascota_registrada.nombre}' registrada con ID: {mascota_registrada.id}, del dueño: {propietario.nombre}.")
            logging.info(f"Mascota: {mascota_registrada.nombre} (ID: {mascota_registrada.id}), del dueño: {propietario.nombre} (ID: {propietario.id}) registrada.")
        else:
            UIUtils.print_message("No se pudo registrar la mascota. Intente nuevamente.")

    def registrar_consulta(self):
        UIUtils.print_title("Registro de Consulta")
        mascota = self._get_mascota("Ingrese el ID de la mascota para la consulta: ")
        if not mascota:
            return

        print(f"Registrando consulta para: {mascota.nombre} (ID: {mascota.id})")
        fecha = UIUtils.get_date_input("Fecha de la consulta (dd-mm-aaaa): ")
        motivo = input("Motivo de la consulta: ")
        diagnostico = input("Diagnóstico: ")

        consulta = Consulta(fecha, motivo, diagnostico, mascota.id)
        consulta_registrada = self.db_manager.insert_consulta(consulta)
        if consulta_registrada:
            print("Consulta registrada con éxito.")
            logging.info(f"Consulta (ID: {consulta_registrada.id}) de la mascota: {mascota.nombre} (ID: {mascota.id}) registrada.")
        else:
            UIUtils.print_message("No se pudo registrar la consulta.")

    def listar_propietarios(self):
        UIUtils.print_title("Lista de Propietarios")
        propietarios = self.db_manager.get_all_propietarios()
        if not propietarios:
            UIUtils.print_message("No existen propietarios registrados.")
            logging.info("Lista de propietarios consultada: No hay registros.")
            return

        for prop in propietarios:
            print(prop)
            print("-" * 30)
        logging.info("Propietarios registrados consultados.")

    def listar_mascotas(self):
        UIUtils.print_title("Lista de Mascotas Registradas")
        mascotas = self.db_manager.get_all_mascotas()
        if not mascotas:
            UIUtils.print_message("No existen mascotas registradas.")
            logging.info("Lista de mascotas consultada: No hay registros.")
            return

        for mascota in mascotas:
            print(mascota)
            print("-" * 30)
        logging.info("Mascotas registradas consultadas.")

    def historia_clinica(self):
        UIUtils.print_title("Historia Clínica")
        mascota = self._get_mascota("Ingrese el ID de la mascota para ver su historial: ")
        if not mascota:
            return

        consultas = self.db_manager.get_consultas_by_mascota_id(mascota.id)
        if not consultas:
            UIUtils.print_message(f"No hay consultas registradas para {mascota.nombre} (ID: {mascota.id}).")
            logging.info(f"No se encontraron consultas para la mascota ID: {mascota.id}.")
            return

        print(f"\nHistorial clínico de {mascota.nombre} (ID: {mascota.id}):")
        for consulta in consultas:
            print(consulta)
            print("-" * 30)
        logging.info(f"Historia clínica de la mascota ID: {mascota.id} consultada.")

    def actualizar_propietario(self):
        UIUtils.print_title("Actualizar Propietario")
        propietario = self._get_propietario("Ingrese el ID del propietario a actualizar: ")
        if not propietario:
            return

        UIUtils.print_message(f"Propietario actual:\n{propietario}")
        print("\nIngrese los nuevos datos (deje en blanco para mantener el actual):")
        new_data = {}

        nombre = input(f"Nuevo nombre ({propietario.nombre}): ").strip()
        if nombre:
            existente = self.db_manager.get_propietario_by_nombre(nombre)
            if existente and existente.id != propietario.id:
                print(f"Error: El nombre '{nombre}' ya está siendo usado por otro propietario (ID: {existente.id}).")
                logging.warning(f"Intento de actualizar propietario ID {propietario.id} a nombre duplicado: {nombre}")
                return
            new_data['nombre'] = nombre

        telefono = input(f"Nuevo teléfono ({propietario.telefono}): ").strip()
        if telefono:
            new_data['telefono'] = telefono

        direccion = input(f"Nueva dirección ({propietario.direccion}): ").strip()
        if direccion:
            new_data['direccion'] = direccion

        if new_data:
            if self.db_manager.update_propietario(propietario.id, new_data):
                print("Propietario actualizado con éxito.")
                logging.info(f"Propietario ID {propietario.id} actualizado.")
            else:
                UIUtils.print_message("No se pudo actualizar el propietario.")
        else:
            UIUtils.print_message("No se ingresaron datos para actualizar.")

    def actualizar_mascota(self):
        UIUtils.print_title("Actualizar Mascota")
        mascota = self._get_mascota("Ingrese el ID de la mascota a actualizar: ")
        if not mascota:
            return

        UIUtils.print_message(f"Mascota actual:\n{mascota}")
        print("\nIngrese los nuevos datos (deje en blanco para mantener el actual):")
        new_data = {}

        nombre = input(f"Nuevo nombre ({mascota.nombre}): ").strip()
        if nombre: new_data['nombre'] = nombre

        especie = input(f"Nueva especie ({mascota.especie}): ").strip()
        if especie: new_data['especie'] = especie

        raza = input(f"Nueva raza ({mascota.raza}): ").strip()
        if raza: new_data['raza'] = raza

        edad_str = input(f"Nueva edad en años ({mascota.edad}): ").strip()
        if edad_str:
            try:
                edad = int(edad_str)
                if edad < 0: raise ValueError
                new_data['edad'] = edad
            except ValueError:
                print("Edad inválida. Se mantendrá la edad actual.")
                logging.warning(f"Intento de actualizar edad de mascota {mascota.id} con valor inválido: '{edad_str}'")

        if UIUtils.confirm_action("¿Desea cambiar el propietario de esta mascota?"):
            nombre_nuevo_propietario = input("Ingrese el nombre del nuevo propietario: ").strip()
            nuevo_propietario = self.db_manager.get_propietario_by_nombre(nombre_nuevo_propietario)
            if nuevo_propietario:
                new_data['id_propietario'] = nuevo_propietario.id
                print(f"Propietario de la mascota cambiado a: {nuevo_propietario.nombre}.")
            else:
                UIUtils.print_message("Propietario no encontrado. No se cambió el propietario.")
                logging.warning(f"Intento de cambiar propietario de mascota {mascota.id} a uno no existente: {nombre_nuevo_propietario}")

        if new_data:
            if self.db_manager.update_mascota(mascota.id, new_data):
                print("Mascota actualizada con éxito.")
                logging.info(f"Mascota ID {mascota.id} actualizada.")
            else:
                UIUtils.print_message("No se pudo actualizar la mascota.")
        else:
            UIUtils.print_message("No se ingresaron datos para actualizar.")

    def actualizar_consulta(self):
        UIUtils.print_title("Actualizar Consulta")
        consulta = self._get_consulta("Ingrese el ID de la consulta a actualizar: ")
        if not consulta:
            return

        UIUtils.print_message(f"Consulta actual (Mascota: {consulta.mascota_nombre}):\n{consulta}")
        print("\nIngrese los nuevos datos (deje en blanco para mantener el actual):")
        new_data = {}

        fecha_str = input(f"Nueva fecha (dd-mm-aaaa) ({consulta.fecha.strftime('%d-%m-%Y')}): ").strip()
        if fecha_str:
            try:
                new_data['fecha'] = datetime.strptime(fecha_str, "%d-%m-%Y").date()
            except ValueError:
                print("Formato de fecha incorrecto. Se mantendrá la fecha actual.")
                logging.warning(f"Intento de actualizar fecha de consulta {consulta.id} con formato inválido: {fecha_str}")

        motivo = input(f"Nuevo motivo ({consulta.motivo}): ").strip()
        if motivo: new_data['motivo'] = motivo

        diagnostico = input(f"Nuevo diagnóstico ({consulta.diagnostico}): ").strip()
        if diagnostico: new_data['diagnostico'] = diagnostico

        if new_data:
            if self.db_manager.update_consulta(consulta.id, new_data):
                print("Consulta actualizada con éxito.")
                logging.info(f"Consulta ID {consulta.id} actualizada.")
            else:
                UIUtils.print_message("No se pudo actualizar la consulta.")
        else:
            UIUtils.print_message("No se ingresaron datos para actualizar.")

    def eliminar_propietario(self):
        UIUtils.print_title("Eliminar Propietario")
        propietario = self._get_propietario("Ingrese el ID del propietario a eliminar: ")
        if not propietario: return

        if UIUtils.confirm_action(f"¿Está seguro de eliminar al propietario '{propietario.nombre}' (ID: {propietario.id})? Esto también eliminará SUS MASCOTAS y todas sus CONSULTAS."):
            if self.db_manager.delete_propietario(propietario.id):
                print("Propietario y sus datos asociados eliminados con éxito.")
                logging.info(f"Propietario ID {propietario.id} y datos asociados eliminados.")
            else:
                UIUtils.print_message("No se pudo eliminar el propietario.")
        else:
            print("Operación cancelada.")
            logging.info(f"Eliminación de propietario ID {propietario.id} cancelada.")

    def eliminar_mascota(self):
        UIUtils.print_title("Eliminar Mascota")
        mascota = self._get_mascota("Ingrese el ID de la mascota a eliminar: ")
        if not mascota: return

        if UIUtils.confirm_action(f"¿Está seguro de eliminar a la mascota '{mascota.nombre}' (ID: {mascota.id})? Esto también eliminará todas sus CONSULTAS."):
            if self.db_manager.delete_mascota(mascota.id):
                print("Mascota y sus consultas eliminadas con éxito.")
                logging.info(f"Mascota ID {mascota.id} y consultas asociadas eliminadas.")
            else:
                UIUtils.print_message("No se pudo eliminar la mascota.")
        else:
            print("Operación cancelada.")
            logging.info(f"Eliminación de mascota ID {mascota.id} cancelada.")

    def eliminar_consulta(self):
        UIUtils.print_title("Eliminar Consulta")
        consulta = self._get_consulta("Ingrese el ID de la consulta a eliminar: ")
        if not consulta: return

        if UIUtils.confirm_action(f"¿Está seguro de eliminar la consulta con ID: {consulta.id} para la mascota '{consulta.mascota_nombre}'?"):
            if self.db_manager.delete_consulta(consulta.id):
                print("Consulta eliminada con éxito.")
                logging.info(f"Consulta ID {consulta.id} eliminada.")
            else:
                UIUtils.print_message("No se pudo eliminar la consulta.")
        else:
            print("Operación cancelada.")
            logging.info(f"Eliminación de consulta ID {consulta.id} cancelada.")

    def cerrar_sistema(self):
        self.db_manager.close_connection()