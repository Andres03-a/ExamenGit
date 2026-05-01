import json
import os
from typing import List, Optional
from modelos.servicio import Servicio

class RepositorioJSON:
    """Maneja todas las operaciones de almacenamiento en JSON"""
    
    def __init__(self, archivo: str):
        self.archivo = archivo
        self._crear_directorio_si_no_existe()
    
    def _crear_directorio_si_no_existe(self):
        """Crea el directorio para el archivo si no existe"""
        directorio = os.path.dirname(self.archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
    
    def cargar_todos(self) -> List[Servicio]:
        """Carga todos los servicios desde el archivo JSON"""
        if not os.path.exists(self.archivo):
            return []
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                return [Servicio.from_dict(servicio) for servicio in datos]
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"⚠️ Error al cargar datos: {e}")
            return []
    
    def guardar_todos(self, servicios: List[Servicio]) -> bool:
        """Guarda todos los servicios en el archivo JSON"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as archivo:
                datos = [servicio.to_dict() for servicio in servicios]
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False
    
    def guardar_servicio(self, servicio: Servicio) -> bool:
        """Guarda un solo servicio (útil para actualizaciones)"""
        servicios = self.cargar_todos()
        
        for i, s in enumerate(servicios):
            if s.id == servicio.id:
                servicios[i] = servicio
                return self.guardar_todos(servicios)
        
        servicios.append(servicio)
        return self.guardar_todos(servicios)
    
    def eliminar_servicio(self, servicio_id: int) -> bool:
        """Elimina un servicio por ID"""
        servicios = self.cargar_todos()
        servicios_filtrados = [s for s in servicios if s.id != servicio_id]
        
        if len(servicios_filtrados) == len(servicios):
            return False
        
        return self.guardar_todos(servicios_filtrados)