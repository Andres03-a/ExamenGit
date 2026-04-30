from datetime import datetime
from typing import Dict, Any

class Servicio:
    """Clase que representa un servicio fotográfico"""
    
    def _init_(self, nombre: str, precio: float, tipo_evento: str, 
                 duracion: float, id_servicio: int = None):
        self.id = id_servicio
        self.nombre = nombre
        self.precio = float(precio)
        self.tipo_evento = tipo_evento
        self.duracion = float(duracion)
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fecha_modificacion = None
    
    def actualizar(self, nombre: str = None, precio: float = None,
                   tipo_evento: str = None, duracion: float = None):
        """Actualiza los atributos del servicio"""
        if nombre:
            self.nombre = nombre
        if precio:
            self.precio = float(precio)
        if tipo_evento:
            self.tipo_evento = tipo_evento
        if duracion:
            self.duracion = float(duracion)
        self.fecha_modificacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el servicio a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "tipo_evento": self.tipo_evento,
            "duracion": self.duracion,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion
        }
    
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> 'Servicio':
        """Crea un servicio desde un diccionario"""
        servicio = cls(
            nombre=datos["nombre"],
            precio=datos["precio"],
            tipo_evento=datos["tipo_evento"],
            duracion=datos["duracion"],
            id_servicio=datos["id"]
        )
        servicio.fecha_creacion = datos.get("fecha_creacion", servicio.fecha_creacion)
        servicio.fecha_modificacion = datos.get("fecha_modificacion")
        return servicio
    
    def _str_(self) -> str:
        return f"{self.nombre} - ${self.precio:,.2f} ({self.duracion}h) - {self.tipo_evento}"
    
    def mostrar_info(self) -> str:
        """Retorna información formateada del servicio"""
        return f"""
 ID: {self.id}
 Nombre: {self.nombre}
 Precio: ${self.precio:,.2f}
 Tipo: {self.tipo_evento}
 Duración: {self.duracion} horas
 Creado: {self.fecha_creacion}
{f' Modificado: {self.fecha_modificacion}' if self.fecha_modificacion else ''}
"""