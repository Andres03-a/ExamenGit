
from datos.repositorio_json import RepositorioJSON
from servicios.gestor_servicios import GestorServicios
from ui.consola import InterfazConsola
import config

def main():
    """Punto de entrada principal de la aplicación"""
    try:
        repositorio = RepositorioJSON(config.ARCHIVO_DATOS)
        gestor = GestorServicios(repositorio)
        interfaz = InterfazConsola(gestor)
        
        print("\n🚀 Iniciando Sistema de Gestión de Servicios Fotográficos...")
        interfaz.ejecutar()
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())