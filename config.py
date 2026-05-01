import os

ARCHIVO_DATOS = "datos/servicios_fotograficos.json"
TIPOS_EVENTO_VALIDOS = ["boda", "retrato", "producto", "deportes", 
                        "eventos", "paisaje", "arquitectura", "otro"]


MENSAJES = {
    "error_archivo": "❌ Error al leer el archivo JSON",
    "exito_guardado": "💾 Datos guardados exitosamente",
    "error_guardado": "❌ Error al guardar datos",
    "servicio_no_encontrado": "❌ Servicio no encontrado",
    "id_invalido": "❌ ID inválido"
}


os.makedirs("datos", exist_ok=True)