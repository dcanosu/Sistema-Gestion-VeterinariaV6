
import logging
from services import SistemaVeterinaria
from ui import UIUtils


# cd C:\Users\Eusse\AppData\Local\Programs\sprint8\djangovet
# py manage.py runserver
# http://127.0.0.1:8000/

def setup_logging():
    """Configura el logging para la aplicación."""
    logging.basicConfig(
        filename="clinica_veterinaria.log",
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def main():
    """Función principal que ejecuta el sistema de la veterinaria."""
    setup_logging()
    logging.info("Se inició la aplicación")
    
    sistema = SistemaVeterinaria()
    
    try:
        while True:
            UIUtils.print_title("Sistema Veterinaria Amigos Peludos")

            print("Gestión de Registros")
            print("1. Registrar nueva mascota")
            print("2. Registrar nueva consulta")
            print("\nConsultar Registros")
            print("3. Ver lista de propietarios")
            print("4. Ver lista de mascotas")
            print("5. Ver historia clínica de una mascota")
            print("\nActualizar Registros")
            print("6. Actualizar propietario")
            print("7. Actualizar mascota")
            print("8. Actualizar consulta")
            print("\nEliminar Registros")
            print("9. Eliminar propietario")
            print("10. Eliminar mascota")
            print("11. Eliminar consulta")
            print("\n12. Salir del sistema")

            opcion = input("\nElija una opción: ").strip()

            opciones = {
                '1': sistema.registrar_mascota,
                '2': sistema.registrar_consulta,
                '3': sistema.listar_propietarios,
                '4': sistema.listar_mascotas,
                '5': sistema.historia_clinica,
                '6': sistema.actualizar_propietario,
                '7': sistema.actualizar_mascota,
                '8': sistema.actualizar_consulta,
                '9': sistema.eliminar_propietario,
                '10': sistema.eliminar_mascota,
                '11': sistema.eliminar_consulta,
            }

            if opcion in opciones:
                opciones[opcion]()
            elif opcion == '12':
                print("¡Gracias por usar el sistema! Hasta luego.")
                logging.info("Se cerró la aplicación")
                break
            else:
                UIUtils.print_message("Opción inválida. Por favor, intente nuevamente.")
            
            # Pausa para que el usuario pueda leer el resultado antes de limpiar la consola o mostrar el menú de nuevo
            if opcion != '12':
                input("\nPresione Enter para continuar...")

    except Exception as e:
        logging.critical(f"Ocurrió un error crítico inesperado: {e}", exc_info=True)
        print(f"\nOcurrió un error inesperado: {e}")
        print("Por favor, revise el archivo de log 'clinica_veterinaria.log' para más detalles.")
    finally:
        sistema.cerrar_sistema()

if __name__ == "__main__":
    main()