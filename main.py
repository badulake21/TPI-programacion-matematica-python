import csv

ARCHIVO_CSV = "paises.csv"
def leer_paises():
    paises = []

    try:
        with open(ARCHIVO_CSV, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                try:
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"].strip(),
                    }

                    if pais["nombre"] and pais["continente"]:
                        paises.append(pais)
                    else:
                        print("Se ignoró una fila con campos vacíos.")
                except (ValueError, KeyError):
                    print("Se ignoró una fila con formato incorrecto.")
    except FileNotFoundError:
        print("No se encontró el archivo paises.csv. Se iniciará con una lista vacía.")

    return paises

def guardar_paises(paises):
    with open(ARCHIVO_CSV, "w", encoding="utf-8", newline="") as archivo:
        campos = ["nombre", "poblacion", "superficie", "continente"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(paises)

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El campo no puede estar vacío.")

def pedir_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= 0:
                return numero
            print("El numero debe ser mayor o igual a 0.")
        except ValueError:
            print("Debe ingresar un numero entero válido.")

def mostrar_paises(paises):
    if not paises:
        print("No hay países para mostrar.")
        return

    for pais in paises:
        print(
            f"{pais['nombre']} | Población: {pais['poblacion']} | "
            f"Superficie: {pais['superficie']} km2 | Continente: {pais['continente']}"
        )

def agregar_pais(paises):
    print("\nAgregar país")
    nombre = pedir_texto("Nombre: ")
    poblacion = pedir_entero("Población: ")
    superficie = pedir_entero("Superficie en km2: ")
    continente = pedir_texto("Continente: ")

    paises.append(
        {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente,
        }
    )
    guardar_paises(paises)
    print("País agregado correctamente.")

def buscar_paises(paises):
    texto = pedir_texto("Ingrese el nombre o parte del nombre: ").lower()
    resultados = []

    for pais in paises:
        if texto in pais["nombre"].lower():
            resultados.append(pais)

    mostrar_paises(resultados)

def actualizar_pais(paises):
    nombre = pedir_texto("Ingrese el nombre exacto del país a actualizar: ").lower()

    for pais in paises:
        if pais["nombre"].lower() == nombre:
            pais["poblacion"] = pedir_entero("Nueva población: ")
            pais["superficie"] = pedir_entero("Nueva superficie en km2: ")
            guardar_paises(paises)
            print("País actualizado correctamente.")
            return

    print("No se encontro un país con ese nombre.")

def filtrar_por_continente(paises):
    continente = pedir_texto("Continente: ").lower()
    resultados = []

    for pais in paises:
        if pais["continente"].lower() == continente:
            resultados.append(pais)

    mostrar_paises(resultados)

def filtrar_por_rango(paises, campo):
    minimo = pedir_entero("Valor mínimo: ")
    maximo = pedir_entero("Valor máximo: ")

    if minimo > maximo:
        print("El mínimo no puede ser mayor que el máximo.")
        return

    resultados = []
    for pais in paises:
        if minimo <= pais[campo] <= maximo:
            resultados.append(pais)

    mostrar_paises(resultados)

def ordenar_paises(paises):
    print("\nOrdenar por:")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    opcion = input("Opcion: ").strip()

    campos = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    campo = campos.get(opcion)

    if campo is None:
        print("Opción inválida.")
        return

    direccion = input("Ascendente (A) o Descendente (D): ").strip().lower()
    descendente = direccion == "d"

    ordenados = sorted(paises, key=lambda pais: pais[campo], reverse=descendente)
    mostrar_paises(ordenados)

def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos para calcular estadísticas.")
        return

    mayor_poblacion = max(paises, key=lambda pais: pais["poblacion"])
    menor_poblacion = min(paises, key=lambda pais: pais["poblacion"])
    promedio_poblacion = sum(pais["poblacion"] for pais in paises) / len(paises)
    promedio_superficie = sum(pais["superficie"] for pais in paises) / len(paises)
    cantidad_por_continente = {}

    for pais in paises:
        continente = pais["continente"]
        cantidad_por_continente[continente] = cantidad_por_continente.get(continente, 0) + 1

    print(f"País con mayor población: {mayor_poblacion['nombre']}")
    print(f"País con menor población: {menor_poblacion['nombre']}")
    print(f"Promedio de población: {promedio_poblacion:.2f}")
    print(f"Promedio de superficie: {promedio_superficie:.2f} km2")
    print("Cantidad de países por continente:")

    for continente, cantidad in cantidad_por_continente.items():
        print(f"- {continente}: {cantidad}")

def mostrar_menu():
    print("\nSistema de gestión de países.")
    print("1. Mostrar todos los países.")
    print("2. Agregar país.")
    print("3. Actualizar país.")
    print("4. Buscar país por nombre.")
    print("5. Filtrar por continente.")
    print("6. Filtrar por rango de población.")
    print("7. Filtrar por rango de superficie.")
    print("8. Ordenar países.")
    print("9. Mostrar estadísticas.")
    print("0. Salir.")

def main():
    paises = leer_paises()

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            mostrar_paises(paises)
        elif opcion == "2":
            agregar_pais(paises)
        elif opcion == "3":
            actualizar_pais(paises)
        elif opcion == "4":
            buscar_paises(paises)
        elif opcion == "5":
            filtrar_por_continente(paises)
        elif opcion == "6":
            filtrar_por_rango(paises, "poblacion")
        elif opcion == "7":
            filtrar_por_rango(paises, "superficie")
        elif opcion == "8":
            ordenar_paises(paises)
        elif opcion == "9":
            mostrar_estadisticas(paises)
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
