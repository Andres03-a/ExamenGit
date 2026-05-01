from typing import List
from modelos.servicio import Servicio
from servicios.gestor_servicios import GestorServicios

class InterfazConsola:
    """Maneja toda la interacción con el usuario por consola"""
    
    def __init__(self, gestor: GestorServicios):
        self.gestor = gestor
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "="*60)
        print("📸 SISTEMA DE GESTIÓN DE SERVICIOS FOTOGRÁFICOS")
        print("="*60)
        print("1. ➕ Agregar servicio")
        print("2. ✏️ Editar servicio")
        print("3. 🗑️ Eliminar servicio")
        print("4. 📋 Listar todos los servicios")
        print("5. 🔍 Buscar servicios")
        print("6. 📊 Ver estadísticas")
        print("7. 🔄 Recargar datos")
        print("8. 🚪 Salir")
        print("-"*60)
    
    def mostrar_submenu_busqueda(self):
        """Muestra el submenú de búsqueda"""
        print("\n--- SUBMENÚ DE BÚSQUEDA ---")
        print("1. Buscar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por tipo de evento")
        print("4. Volver al menú principal")
    
    def agregar_servicio_interfaz(self):
        """Interfaz para agregar un servicio"""
        print("\n--- AGREGAR NUEVO SERVICIO ---")
        
        try:
            nombre = input("Nombre del paquete: ").strip()
            if not nombre:
                print("❌ El nombre es obligatorio")
                return
            
            precio = float(input("Precio: ").strip())
            tipo_evento = input("Tipo de evento (boda, retrato, producto, etc.): ").strip()
            duracion = float(input("Duración estimada (horas): ").strip())
            
            servicio = self.gestor.agregar_servicio(nombre, precio, tipo_evento, duracion)
            print(f"\n✅ Servicio agregado exitosamente!")
            print(servicio.mostrar_info())
            
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def editar_servicio_interfaz(self):
        """Interfaz para editar un servicio"""
        print("\n--- EDITAR SERVICIO ---")
        self.listar_servicios_resumido()
        
        try:
            servicio_id = int(input("\nID del servicio a editar: "))
            servicio = self.gestor.buscar_por_id(servicio_id)
            
            if not servicio:
                print("❌ Servicio no encontrado")
                return
            
            print("\nDeje en blanco los campos que no desea modificar")
            print(f"Nombre actual: {servicio.nombre}")
            nombre = input("Nuevo nombre: ").strip() or None
            
            print(f"Precio actual: ${servicio.precio:,.2f}")
            precio_str = input("Nuevo precio: ").strip()
            precio = float(precio_str) if precio_str else None
            
            print(f"Tipo actual: {servicio.tipo_evento}")
            tipo_evento = input("Nuevo tipo de evento: ").strip() or None
            
            print(f"Duración actual: {servicio.duracion} horas")
            duracion_str = input("Nueva duración: ").strip()
            duracion = float(duracion_str) if duracion_str else None
            
            if self.gestor.editar_servicio(servicio_id, nombre, precio, tipo_evento, duracion):
                print(f"\n✅ Servicio {servicio_id} actualizado exitosamente!")
                servicio_actualizado = self.gestor.buscar_por_id(servicio_id)
                print(servicio_actualizado.mostrar_info())
            else:
                print("❌ Error al actualizar el servicio")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def eliminar_servicio_interfaz(self):
        """Interfaz para eliminar un servicio"""
        print("\n--- ELIMINAR SERVICIO ---")
        self.listar_servicios_resumido()
        
        try:
            servicio_id = int(input("\nID del servicio a eliminar: "))
            servicio = self.gestor.buscar_por_id(servicio_id)
            
            if not servicio:
                print("❌ Servicio no encontrado")
                return
            
            print(f"\nServicio a eliminar: {servicio.nombre}")
            confirmar = input("¿Está seguro? (s/n): ").lower()
            
            if confirmar == 's':
                if self.gestor.eliminar_servicio(servicio_id):
                    print(f"✅ Servicio '{servicio.nombre}' eliminado exitosamente!")
                else:
                    print("❌ Error al eliminar el servicio")
                    
        except ValueError:
            print("❌ ID inválido")
    
    def listar_servicios_completo(self):
        """Muestra todos los servicios con detalles completos"""
        servicios = self.gestor.listar_todos()
        
        if not servicios:
            print("\n📭 No hay servicios registrados")
            return
        
        print("\n" + "="*80)
        print("📸 LISTA COMPLETA DE SERVICIOS")
        print("="*80)
        
        for servicio in servicios:
            print(servicio.mostrar_info())
            print("-" * 40)
    
    def listar_servicios_resumido(self):
        """Muestra lista resumida de servicios"""
        servicios = self.gestor.listar_todos()
        
        if not servicios:
            print("\n📭 No hay servicios registrados")
            return
        
        print("\n📋 LISTA DE SERVICIOS:")
        for servicio in servicios:
            print(f"  [{servicio.id}] {servicio}")
    
    def buscar_servicios_interfaz(self):
        """Interfaz para búsqueda de servicios"""
        while True:
            self.mostrar_submenu_busqueda()
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                self.buscar_por_id_interfaz()
            elif opcion == "2":
                self.buscar_por_nombre_interfaz()
            elif opcion == "3":
                self.buscar_por_tipo_interfaz()
            elif opcion == "4":
                break
            else:
                print("❌ Opción inválida")
            
            input("\nPresione Enter para continuar...")
    
    def buscar_por_id_interfaz(self):
        """Búsqueda por ID"""
        try:
            servicio_id = int(input("\nID del servicio: "))
            servicio = self.gestor.buscar_por_id(servicio_id)
            
            if servicio:
                print("\n✅ Servicio encontrado:")
                print(servicio.mostrar_info())
            else:
                print("❌ Servicio no encontrado")
        except ValueError:
            print("❌ ID inválido")
    
    def buscar_por_nombre_interfaz(self):
        """Búsqueda por nombre"""
        nombre = input("\nNombre (o parte) a buscar: ").strip()
        resultados = self.gestor.buscar_por_nombre(nombre)
        
        if resultados:
            print(f"\n✅ Encontrados {len(resultados)} servicio(s):")
            for servicio in resultados:
                print(f"  • {servicio}")
        else:
            print("❌ No se encontraron servicios con ese nombre")
    
    def buscar_por_tipo_interfaz(self):
        """Búsqueda por tipo de evento"""
        tipo_evento = input("\nTipo de evento a buscar: ").strip()
        resultados = self.gestor.buscar_por_tipo(tipo_evento)
        
        if resultados:
            print(f"\n✅ Encontrados {len(resultados)} servicio(s) de tipo '{tipo_evento}':")
            for servicio in resultados:
                print(f"  • {servicio}")
        else:
            print(f"❌ No se encontraron servicios de tipo '{tipo_evento}'")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de los servicios"""
        stats = self.gestor.obtener_estadisticas()
        
        if stats["total"] == 0:
            print("\n📭 No hay servicios para mostrar estadísticas")
            return
        
        print("\n" + "="*50)
        print("📊 ESTADÍSTICAS DE SERVICIOS")
        print("="*50)
        print(f"📌 Total de servicios: {stats['total']}")
        print(f"💰 Precio promedio: ${stats['precio_promedio']:,.2f}")
        print(f"💵 Precio mínimo: ${stats['precio_minimo']:,.2f}")
        print(f"💎 Precio máximo: ${stats['precio_maximo']:,.2f}")
        print(f"⏰ Duración promedio: {stats['duracion_promedio']:.1f} horas")
        
        print("\n📋 Distribución por tipo de evento:")
        for tipo, cantidad in stats['tipos_eventos'].items():
            print(f"  • {tipo}: {cantidad} servicio(s)")
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción (1-8): ").strip()
            
            if opcion == "1":
                self.agregar_servicio_interfaz()
            elif opcion == "2":
                self.editar_servicio_interfaz()
            elif opcion == "3":
                self.eliminar_servicio_interfaz()
            elif opcion == "4":
                self.listar_servicios_completo()
            elif opcion == "5":
                self.buscar_servicios_interfaz()
            elif opcion == "6":
                self.mostrar_estadisticas()
            elif opcion == "7":
                self.gestor.recargar_datos()
                print("✅ Datos recargados exitosamente")
            elif opcion == "8":
                print("\n👋 ¡Gracias por usar el sistema!")
                break
            else:
                print("❌ Opción inválida")
            
            if opcion != "5": 
                input("\nPresione Enter para continuar...")