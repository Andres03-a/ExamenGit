import json
import os

ARCHIVO = "servicios.json"


def cargar_servicios():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


def guardar_servicios(servicios):
    with open(ARCHIVO, "w") as f:
        json.dump(servicios, f, indent=4)


# =========================
# REGISTRAR SERVICIO
# =========================
def registrar():
    print("=== Registro de Servicios ===")

    nombre = input("Nombre del paquete fotográfico: ")

    try:
        precio = float(input("Precio del servicio: "))
    except ValueError:
        print("Error: El precio debe ser un número.\n")
        return

    tipo_evento = input("Tipo de evento (boda, retrato, producto, etc.): ")

    try:
        duracion = float(input("Duración estimada (en horas): "))
    except ValueError:
        print("Error: La duración debe ser un número.\n")
        return

    servicios = cargar_servicios()

    nuevo_servicio = {
        "nombre": nombre,
        "precio": precio,
        "tipo_evento": tipo_evento,
        "duracion": duracion
    }

    servicios.append(nuevo_servicio)

    guardar_servicios(servicios)

    print("✔ Servicio registrado correctamente.\n")


# =========================
# EDITAR SERVICIO
# =========================
def editar_servicio():
    servicios = cargar_servicios()

    if not servicios:
        print("No hay servicios registrados.\n")
        return

    print("=== Lista de Servicios ===")
    for i, s in enumerate(servicios):
        print(f"{i + 1}. {s['nombre']} - {s['tipo_evento']} - ${s['precio']}")

    try:
        opcion = int(input("Seleccione el número del servicio a editar: ")) - 1
        if opcion < 0 or opcion >= len(servicios):
            print("Opción inválida.\n")
            return
    except ValueError:
        print("Debe ingresar un número.\n")
        return

    servicio = servicios[opcion]

    print("\n--- Editando servicio ---")

    nuevo_nombre = input(f"Nombre ({servicio['nombre']}): ") or servicio['nombre']
    
    try:
        nuevo_precio = input(f"Precio ({servicio['precio']}): ")
        nuevo_precio = float(nuevo_precio) if nuevo_precio else servicio['precio']
    except ValueError:
        print("Precio inválido.\n")
        return

    nuevo_tipo = input(f"Tipo evento ({servicio['tipo_evento']}): ") or servicio['tipo_evento']

    try:
        nueva_duracion = input(f"Duración ({servicio['duracion']}): ")
        nueva_duracion = float(nueva_duracion) if nueva_duracion else servicio['duracion']
    except ValueError:
        print("Duración inválida.\n")
        return

    servicios[opcion] = {
        "nombre": nuevo_nombre,
        "precio": nuevo_precio,
        "tipo_evento": nuevo_tipo,
        "duracion": nueva_duracion
    }

    guardar_servicios(servicios)

    print("✔ Servicio editado correctamente.\n")


# =========================
# ELIMINAR SERVICIO
# =========================
def eliminar_servicio():
    servicios = cargar_servicios()

    if not servicios:
        print("No hay servicios para eliminar.\n")
        return

    print("=== Lista de Servicios ===")
    for i, s in enumerate(servicios):
        print(f"{i + 1}. {s['nombre']} - {s['tipo_evento']}")

    try:
        opcion = int(input("Seleccione el número del servicio a eliminar: ")) - 1
        if opcion < 0 or opcion >= len(servicios):
            print("Opción inválida.\n")
            return
    except ValueError:
        print("Debe ingresar un número.\n")
        return

    confirmacion = input("¿Seguro que quieres eliminar este servicio? (Si/No): ").capitalize()

    if confirmacion == "Si":
        eliminado = servicios.pop(opcion)
        guardar_servicios(servicios)
        print(f"✔ Servicio '{eliminado['nombre']}' eliminado.\n")
    else:
        print("Operación cancelada.\n")