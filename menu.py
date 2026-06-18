import requests
import re
from patient import create_patient_resource
from base import send_resource_to_hapi_fhir

HAPI_BASE_URL = "http://hapi.fhir.org/baseR4"
HEADERS = {"Accept": "application/fhir+json"}

GENEROS_VALIDOS = ["male", "female", "other", "unknown"]


def limpiar():
    print("\n" * 2)


def separador():
    print("─" * 50)


def input_opcional(prompt):
    val = input(prompt).strip()
    return val if val else None


def input_genero():
    while True:
        gender = input("  Género (male / female / other / unknown): ").strip().lower()
        if gender in GENEROS_VALIDOS:
            return gender
        print(f"  ✗ Valor inválido. Ingresá uno de: {', '.join(GENEROS_VALIDOS)}")


def input_fecha(prompt):
    while True:
        fecha = input(prompt).strip()
        if not fecha:
            return None
        if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            return fecha
        print("  ✗ Formato inválido. Usá YYYY-MM-DD (ej: 1995-07-22)")


def input_dni():
    while True:
        dni = input("  DNI (solo números): ").strip()
        if re.match(r"^\d{7,8}$", dni):
            return dni
        print("  ✗ DNI inválido. Debe tener 7 u 8 dígitos.")


def input_telefono():
    while True:
        tel = input("  Teléfono (solo números, opcional — Enter para omitir): ").strip()
        if not tel:
            return None
        if re.match(r"^\d+$", tel):
            return tel
        print("  ✗ Solo se permiten números.")


# ─────────────────────────────────────────
# CREAR PACIENTE
# ─────────────────────────────────────────
def crear_paciente():
    limpiar()
    print("─" * 50)
    print("  CREAR PACIENTE")
    print("─" * 50)

    family_name = input_opcional("  Apellido: ")
    given_name  = input_opcional("  Nombre: ")
    birth_date  = input_fecha("  Fecha de nacimiento (YYYY-MM-DD, opcional — Enter para omitir): ")
    gender      = input_genero()
    phone       = input_telefono()
    dni         = input_dni()

    patient = create_patient_resource(
        family_name=family_name,
        given_name=given_name,
        birth_date=birth_date,
        gender=gender,
        phone=phone,
        dni=dni,
    )

    separador()
    print("  Creando paciente en HAPI FHIR...")
    patient_id = send_resource_to_hapi_fhir(patient, "Patient")

    if patient_id:
        url = f"{HAPI_BASE_URL}/Patient/{patient_id}"
        print(f"\n  ✓ Paciente creado exitosamente")
        print(f"  ID asignado: {patient_id}")
        print(f"  URL FHIR:    {url}")
    else:
        print(f"\n  ✗ No se pudo crear el paciente (puede que ya exista ese DNI)")

    separador()
    input("  Presioná Enter para volver al menú principal...")


# ─────────────────────────────────────────
# MOSTRAR ALERGIAS
# ─────────────────────────────────────────
def mostrar_alergias(patient_id):
    url = f"{HAPI_BASE_URL}/AllergyIntolerance"
    params = {"patient": patient_id}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("\n  ✗ Error al buscar alergias")
        return

    bundle = response.json()
    total = bundle.get("total", 0)
    entries = bundle.get("entry", [])

    separador()
    if total == 0:
        print("  Sin alergias registradas para este paciente.")
        return

    print(f"  ALERGIAS REGISTRADAS ({total})")
    separador()

    for i, entry in enumerate(entries, 1):
        r = entry.get("resource", {})
        allergy_id = r.get("id")
        allergy_url = f"{HAPI_BASE_URL}/AllergyIntolerance/{allergy_id}"

        # Sustancia
        code = r.get("code", {})
        sustancia = code.get("text") or (
            code.get("coding", [{}])[0].get("display", "Sin especificar")
        )

        # Estado clínico
        clinical = r.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "-")

        # Criticidad y tipo
        criticality  = r.get("criticality", "-")
        allergy_type = r.get("type", "-")

        # Reacciones
        reactions = r.get("reaction", [])

        print(f"\n  [{i}] {sustancia}")
        print(f"      Estado:      {clinical}")
        print(f"      Tipo:        {allergy_type}")
        print(f"      Criticidad:  {criticality}")

        if reactions:
            for j, reaction in enumerate(reactions, 1):
                severity = reaction.get("severity", "-")
                manifestations = reaction.get("manifestation", [])
                for m in manifestations:
                    manifestacion = m.get("text") or (
                        m.get("coding", [{}])[0].get("display", "-")
                    )
                    print(f"      Reacción {j}:   {manifestacion} ({severity})")

        notes = r.get("note", [])
        if notes:
            print(f"      Nota:        {notes[0].get('text', '-')}")

        print(f"      URL FHIR:    {allergy_url}")


# ─────────────────────────────────────────
# BUSCAR PACIENTE POR DNI
# ─────────────────────────────────────────
def buscar_paciente():
    limpiar()
    print("─" * 50)
    print("  BUSCAR PACIENTE POR DNI")
    print("─" * 50)

    while True:
        print("  (escribí 'volver' para ir al menú principal)")
        dni = input("  DNI: ").strip()

        if dni.lower() == "volver":
            return

        if not re.match(r"^\d{7,8}$", dni):
            print("  ✗ DNI inválido. Debe tener 7 u 8 dígitos.\n")
            continue

        url = f"{HAPI_BASE_URL}/Patient"
        params = {"identifier": f"http://www.renaper.gob.ar/dni|{dni}"}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("  ✗ Error en la búsqueda. Intentá de nuevo.")
            continue

        bundle = response.json()
        entries = bundle.get("entry", [])

        if not entries:
            print(f"\n  ✗ No se encontró ningún paciente con DNI {dni}\n")
            continue

        patient    = entries[0]["resource"]
        patient_id = patient.get("id")
        patient_url = f"{HAPI_BASE_URL}/Patient/{patient_id}"

        # Nombre
        names = patient.get("name", [])
        if names:
            given  = " ".join(names[0].get("given", []))
            family = names[0].get("family", "")
            nombre = f"{given} {family}".strip()
        else:
            nombre = "Sin nombre"

        birth_date = patient.get("birthDate", "-")
        gender     = patient.get("gender", "-")

        separador()
        print(f"\n  ✓ Paciente encontrado")
        print(f"  Nombre:     {nombre}")
        print(f"  DNI:        {dni}")
        print(f"  Nacimiento: {birth_date}")
        print(f"  Género:     {gender}")
        print(f"  ID FHIR:    {patient_id}")
        print(f"  URL FHIR:   {patient_url}")

        # Submenú
        while True:
            separador()
            print("  ¿Qué querés hacer?")
            print("  1) Ver alergias")
            print("  2) Buscar otro paciente")
            print("  3) Volver al menú principal")
            separador()
            opcion = input("  Opción: ").strip()

            if opcion == "1":
                mostrar_alergias(patient_id)
                input("\n  Presioná Enter para continuar...")
            elif opcion == "2":
                break
            elif opcion == "3":
                return
            else:
                print("  Opción inválida.")


# ─────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────
def menu_principal():
    while True:
        limpiar()
        print("═" * 50)
        print("  SISTEMA FHIR — AllergyIntolerance TP6")
        print("═" * 50)
        print("  1) Crear paciente")
        print("  2) Buscar paciente por DNI")
        print("  3) Salir")
        print("═" * 50)
        opcion = input("  Opción: ").strip()

        if opcion == "1":
            crear_paciente()
        elif opcion == "2":
            buscar_paciente()
        elif opcion == "3":
            print("\n  Hasta luego.\n")
            break
        else:
            print("  Opción inválida.")


if __name__ == "__main__":
    menu_principal()
