# ui.py
from datetime import datetime
import logging

class UIUtils:
    """Clase estática para utilidades de interfaz de usuario en consola."""
    @staticmethod
    def print_title(text):
        print("\n" + "=" * 60)
        print(f"{text.center(60)}")
        print("=" * 60 + "\n")

    @staticmethod
    def print_message(text):
        print("\n * " + text)

    @staticmethod
    def get_int_input(prompt, error_msg="Entrada inválida. Por favor, ingrese un número."):
        """Solicita una entrada entera al usuario con manejo de errores."""
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print(error_msg)
                logging.error(f"Entrada no numérica: '{prompt.strip()}'")

    @staticmethod
    def get_date_input(prompt, error_msg="Formato de fecha incorrecto. Use dd-mm-aaaa. Ejemplo: 05-06-2025."):
        """Solicita una fecha al usuario en formato dd-mm-aaaa con manejo de errores."""
        while True:
            date_str = input(prompt).strip()
            try:
                return datetime.strptime(date_str, "%d-%m-%Y").date()
            except ValueError:
                print(error_msg)
                logging.error(f"Formato de fecha inválido: '{date_str}'")

    @staticmethod
    def confirm_action(prompt):
        """Solicita confirmación al usuario para una acción."""
        while True:
            confirm = input(prompt + " (s/n): ").strip().lower()
            if confirm in ['s', 'n']:
                return confirm == 's'
            else:
                print("Respuesta inválida. Por favor, ingrese 's' o 'n'.")