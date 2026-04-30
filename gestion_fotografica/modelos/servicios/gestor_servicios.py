from typing import List, Optional, Dict
from modelos.servicio import Servicio
from datos.repositorio_json import RepositorioJSON

class GestorServicios:
    """Gestiona la lógica de negocio de los servicios fotográficos"""
    
    def _init_(self, repositorio: RepositorioJSON):
        self.repositorio = repositorio
        self.servicios = self.repositorio.cargar_todos()
        self._contador_id = self._obtener_maximo_id()
    
    def _obtener_maximo_id(self) -> int:
        """Obtiene el máximo ID usado"""
        if not self.servicios:
            return 0
        return max(servicio.id for servicio in self.servicios)
    
    def _generar_id(self) -> int:
        """Genera un nuevo ID"""
        self._contador_id += 1
        return self._contador_id
    
    def _servicio_existe(self, nombre: str, id_excluir: int = None) -> bool:
        """Verifica si ya existe un servicio con el mismo nombre"""
        for servicio in self.servicios:
            if servicio.nombre.lower() == nombre.lower():
                if id_excluir is None or servicio.id != id_excluir:
                    return True
        return False
    
    def agregar_servicio(self, nombre: str, precio: float, 
                         tipo_evento: str, duracion: float) -> Optional[Servicio]:
        """Agrega un nuevo servicio"""
        # Validaciones
        if not nombre or not tipo_evento:
            raise ValueError("Nombre y tipo de evento son obligatorios")
        
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a 0")
        
        if self._servicio_existe(nombre):
            raise ValueError(f"Ya existe un servicio con el nombre '{nombre}'")
        
        # Crear servicio
        nuevo_servicio = Servicio(
            nombre=nombre,
            precio=precio,
            tipo_evento=tipo_evento,
            duracion=duracion,
            id_servicio=self._generar_id()
        )
        
        # Guardar
        self.servicios.append(nuevo_servicio)
        if self.repositorio.guardar_servicio(nuevo_servicio):
            return nuevo_servicio
        else:
            self.servicios.pop()  # Revertir cambios
            raise Exception("Error al guardar en el repositorio")
    
    def editar_servicio(self, servicio_id: int, nombre: str = None,
                        precio: float = None, tipo_evento: str = None,
                        duracion: float = None) -> bool:
        """Edita un servicio existente"""
        servicio = self.buscar_por_id(servicio_id)
        if not servicio:
            return False
        
        # Validar nombre único si se cambia
        if nombre and nombre != servicio.nombre:
            if self._servicio_existe(nombre, servicio_id):
                raise ValueError(f"Ya existe otro servicio con el nombre '{nombre}'")
        
        # Validar valores positivos
        if precio and precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if duracion and duracion <= 0:
            raise ValueError("La duración debe ser mayor a 0")
        
        # Actualizar
        servicio.actualizar(
            nombre=nombre,
            precio=precio,
            tipo_evento=tipo_evento,
            duracion=duracion
        )
        
        return self.repositorio.guardar_servicio(servicio)
    
    def eliminar_servicio(self, servicio_id: int) -> bool:
        """Elimina un servicio"""
        servicio = self.buscar_por_id(servicio_id)
        if not servicio:
            return False
        
        self.servicios = [s for s in self.servicios if s.id != servicio_id]
        return self.repositorio.eliminar_servicio(servicio_id)
    
    def buscar_por_id(self, servicio_id: int) -> Optional[Servicio]:
        """Busca un servicio por ID"""
        for servicio in self.servicios:
            if servicio.id == servicio_id:
                return servicio
        return None
    
    def buscar_por_nombre(self, nombre: str) -> List[Servicio]:
        """Busca servicios por nombre (búsqueda parcial)"""
        nombre_lower = nombre.lower()
        return [s for s in self.servicios if nombre_lower in s.nombre.lower()]
    
    def buscar_por_tipo(self, tipo_evento: str) -> List[Servicio]:
        """Busca servicios por tipo de evento"""
        tipo_lower = tipo_evento.lower()
        return [s for s in self.servicios if s.tipo_evento.lower() == tipo_lower]
    
    def listar_todos(self) -> List[Servicio]:
        """Retorna todos los servicios"""
        return self.servicios.copy()
    
    def obtener_estadisticas(self) -> Dict:
        """Calcula estadísticas de los servicios"""
        if not self.servicios:
            return {"total": 0}
        
        precios = [s.precio for s in self.servicios]
        duraciones = [s.duracion for s in self.servicios]
        
        tipos_eventos = {}
        for servicio in self.servicios:
            tipo = servicio.tipo_evento
            tipos_eventos[tipo] = tipos_eventos.get(tipo, 0) + 1
        
        return {
            "total": len(self.servicios),
            "precio_promedio": sum(precios) / len(precios),
            "precio_minimo": min(precios),
            "precio_maximo": max(precios),
            "duracion_promedio": sum(duraciones) / len(duraciones),
            "tipos_eventos": tipos_eventos
        }
    
    def recargar_datos(self):
        """Recarga los datos desde el archivo"""
        self.servicios = self.repositorio.cargar_todos()
        self._contador_id = self._obtener_maximo_id()