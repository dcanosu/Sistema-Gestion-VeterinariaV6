# database.py
import sqlite3
import logging
from datetime import date
from models import Propietario, Mascota, Consulta

class DatabaseManager:
    def __init__(self, db_name="clinica_veterinaria.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Conexión a la base de datos {self.db_name} establecida.")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            print(f"Error al conectar a la base de datos: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logging.info(f"Conexión a la base de datos {self.db_name} cerrada.")

    def create_tables(self):
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON;") # Habilita la integridad referencial
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS propietarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    telefono TEXT,
                    direccion TEXT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS mascotas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    especie TEXT,
                    raza TEXT,
                    edad INTEGER,
                    id_propietario INTEGER,
                    FOREIGN KEY (id_propietario) REFERENCES propietarios(id) ON DELETE CASCADE
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS consultas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    motivo TEXT,
                    diagnostico TEXT,
                    id_mascota INTEGER,
                    FOREIGN KEY (id_mascota) REFERENCES mascotas(id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
            logging.info("Tablas creadas o ya existentes.")
        except sqlite3.Error as e:
            logging.error(f"Error al crear tablas: {e}")
            print(f"Error al crear tablas: {e}")

    # --- CRUD Propietario (Sin cambios) ---
    def insert_propietario(self, propietario):
        try:
            self.cursor.execute(
                "INSERT INTO propietarios (nombre, telefono, direccion) VALUES (?, ?, ?)",
                (propietario.nombre, propietario.telefono, propietario.direccion)
            )
            self.conn.commit()
            propietario.id = self.cursor.lastrowid
            logging.info(f"Propietario '{propietario.nombre}' insertado con ID: {propietario.id}")
            return propietario
        except sqlite3.IntegrityError:
            logging.warning(f"Intento de insertar propietario duplicado: {propietario.nombre}")
            return None
        except sqlite3.Error as e:
            logging.error(f"Error al insertar propietario: {e}")
            return None

    def get_propietario_by_nombre(self, nombre):
        try:
            self.cursor.execute("SELECT id, nombre, telefono, direccion FROM propietarios WHERE nombre LIKE ?", (nombre,))
            row = self.cursor.fetchone()
            return Propietario(row[1], row[2], row[3], row[0]) if row else None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar propietario por nombre: {e}")
            return None

    def get_propietario_by_id(self, propietario_id):
        try:
            self.cursor.execute("SELECT id, nombre, telefono, direccion FROM propietarios WHERE id = ?", (propietario_id,))
            row = self.cursor.fetchone()
            return Propietario(row[1], row[2], row[3], row[0]) if row else None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar propietario por ID: {e}")
            return None

    def get_all_propietarios(self):
        try:
            self.cursor.execute("SELECT id, nombre, telefono, direccion FROM propietarios")
            rows = self.cursor.fetchall()
            return [Propietario(row[1], row[2], row[3], row[0]) for row in rows]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener todos los propietarios: {e}")
            return []

    def update_propietario(self, propietario_id, new_data):
        try:
            set_clause = ", ".join([f"{k} = ?" for k in new_data.keys()])
            values = list(new_data.values())
            values.append(propietario_id)
            self.cursor.execute(f"UPDATE propietarios SET {set_clause} WHERE id = ?", tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error al actualizar propietario: {e}")
            return False

    def delete_propietario(self, propietario_id):
        try:
            self.cursor.execute("DELETE FROM propietarios WHERE id = ?", (propietario_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar propietario: {e}")
            return False

    # --- CRUD Mascota (Sin cambios) ---
    def insert_mascota(self, mascota):
        try:
            self.cursor.execute(
                "INSERT INTO mascotas (nombre, especie, raza, edad, id_propietario) VALUES (?, ?, ?, ?, ?)",
                (mascota.nombre, mascota.especie, mascota.raza, mascota.edad, mascota.propietario_id)
            )
            self.conn.commit()
            mascota.id = self.cursor.lastrowid
            logging.info(f"Mascota '{mascota.nombre}' insertada con ID: {mascota.id}")
            return mascota
        except sqlite3.Error as e:
            logging.error(f"Error al insertar mascota: {e}")
            return None

    def get_all_mascotas(self):
        try:
            self.cursor.execute("""
                SELECT m.id, m.nombre, m.especie, m.raza, m.edad, m.id_propietario, p.nombre
                FROM mascotas m
                JOIN propietarios p ON m.id_propietario = p.id
            """)
            rows = self.cursor.fetchall()
            return [Mascota(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) for row in rows]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener todas las mascotas: {e}")
            return []

    def get_mascota_by_id(self, mascota_id):
        try:
            self.cursor.execute("""
                SELECT m.id, m.nombre, m.especie, m.raza, m.edad, m.id_propietario, p.nombre
                FROM mascotas m
                JOIN propietarios p ON m.id_propietario = p.id
                WHERE m.id = ?
            """, (mascota_id,))
            row = self.cursor.fetchone()
            return Mascota(row[1], row[2], row[3], row[4], row[5], row[0], row[6]) if row else None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar mascota por ID: {e}")
            return None

    def update_mascota(self, mascota_id, new_data):
        try:
            set_clause = ", ".join([f"{k} = ?" for k in new_data.keys()])
            values = list(new_data.values())
            values.append(mascota_id)
            self.cursor.execute(f"UPDATE mascotas SET {set_clause} WHERE id = ?", tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error al actualizar mascota: {e}")
            return False

    def delete_mascota(self, mascota_id):
        try:
            self.cursor.execute("DELETE FROM mascotas WHERE id = ?", (mascota_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar mascota: {e}")
            return False

    # --- CRUD Consulta (Con correcciones) ---
    def insert_consulta(self, consulta):
        try:
            self.cursor.execute(
                "INSERT INTO consultas (fecha, motivo, diagnostico, id_mascota) VALUES (?, ?, ?, ?)",
                (consulta.fecha.strftime("%Y-%m-%d"), consulta.motivo, consulta.diagnostico, consulta.mascota_id)
            )
            self.conn.commit()
            consulta.id = self.cursor.lastrowid
            logging.info(f"Consulta para mascota ID {consulta.mascota_id} registrada con ID: {consulta.id}")
            return consulta
        except sqlite3.Error as e:
            logging.error(f"Error al insertar consulta: {e}")
            return None

    def get_consultas_by_mascota_id(self, mascota_id):
        try:
            self.cursor.execute("""
                SELECT c.id, c.fecha, c.motivo, c.diagnostico, c.id_mascota, m.nombre
                FROM consultas c
                JOIN mascotas m ON c.id_mascota = m.id
                WHERE c.id_mascota = ?
                ORDER BY c.fecha DESC
            """, (mascota_id,))
            rows = self.cursor.fetchall()
            return [Consulta(row[1], row[2], row[3], row[4], row[0], row[5]) for row in rows]
        except sqlite3.Error as e:
            logging.error(f"Error al obtener consultas por ID de mascota: {e}")
            return []

    def get_consulta_by_id(self, consulta_id):
        try:
            self.cursor.execute("""
                SELECT c.id, c.fecha, c.motivo, c.diagnostico, c.id_mascota, m.nombre
                FROM consultas c
                JOIN mascotas m ON c.id_mascota = m.id
                WHERE c.id = ?
            """, (consulta_id,))
            row = self.cursor.fetchone()
            return Consulta(row[1], row[2], row[3], row[4], row[0], row[5]) if row else None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar consulta por ID: {e}")
            return None

    def update_consulta(self, consulta_id, new_data):
        """
        ✅ CORREGIDO: Actualiza una consulta de forma segura.
        """
        try:
            # No se modifica el diccionario original, se construye la consulta de forma segura
            fields_to_update = []
            values = []
            for key, value in new_data.items():
                fields_to_update.append(f"{key} = ?")
                # Se asegura que la fecha se formatee a texto si es un objeto 'date'
                if key == 'fecha' and isinstance(value, date):
                    values.append(value.strftime("%Y-%m-%d"))
                else:
                    values.append(value)
            
            if not fields_to_update:
                return True # No hay nada que actualizar

            set_clause = ", ".join(fields_to_update)
            sql_query = f"UPDATE consultas SET {set_clause} WHERE id = ?"
            values.append(consulta_id)

            self.cursor.execute(sql_query, tuple(values))
            self.conn.commit() # Confirma la transacción
            
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error al actualizar consulta: {e}")
            return False

    def delete_consulta(self, consulta_id):
        """
        ✅ CORREGIDO: Elimina una consulta y asegura que se guarde el cambio.
        """
        try:
            self.cursor.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
            self.conn.commit() # Confirma la transacción
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar consulta: {e}")
            return False