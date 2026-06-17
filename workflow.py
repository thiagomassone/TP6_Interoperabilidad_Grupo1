from patient import create_patient_resource
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir, search_patient_by_dni
from allergy_intolerance import create_allergy_intolerance_resource

if __name__ == "__main__":

    # ------------------------------------------------------------------ #
    #  ACTIVIDAD 3a – Crear paciente con DNI e identifier, luego leerlo   #
    # ------------------------------------------------------------------ #
    print("=" * 60)
    print("ACTIVIDAD 3a – Crear y leer paciente con DNI")
    print("=" * 60)

    patient = create_patient_resource(
        family_name="García",
        given_name="Lucía",
        birth_date="1995-07-22",
        gender="female",
        phone="1155443322",
        dni="38123456",
    )

    patient_id = send_resource_to_hapi_fhir(patient, "Patient")

    # Si el paciente ya existe en el servidor, usamos el ID conocido
    if not patient_id:
        patient_id = "137001175"
        print(f"Usando paciente existente con ID: {patient_id}")

    print(f"\nPaciente ID: {patient_id}")
    print("\nLeyendo recurso creado:")
    get_resource_from_hapi_fhir(patient_id, "Patient")

    # ------------------------------------------------------------------ #
    #  ACTIVIDAD 3b – Buscar paciente por documento                       #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("ACTIVIDAD 3b – Buscar paciente por DNI")
    print("=" * 60)

    search_patient_by_dni("38123456")

    # ------------------------------------------------------------------ #
    #  ACTIVIDAD 3c – Crear recurso AllergyIntolerance                    #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("ACTIVIDAD 3c – Crear recurso AllergyIntolerance")
    print("=" * 60)

    allergy = create_allergy_intolerance_resource(
        patient_id=patient_id,
        substance_code="372687004",
        substance_display="Amoxicilina",
        clinical_status="active",
        verification_status="confirmed",
        allergy_type="allergy",
        category="medication",
        criticality="high",
        reaction_manifestation_code="271807003",
        reaction_manifestation_display="Erupción cutánea",
        reaction_severity="moderate",
        note="Paciente refiere reacción alérgica tras primera dosis de amoxicilina en 2018.",
    )

    allergy_id = send_resource_to_hapi_fhir(allergy, "AllergyIntolerance")

    if allergy_id:
        print(f"\nAllergyIntolerance creada con ID: {allergy_id}")
        print("\nLeyendo recurso creado:")
        get_resource_from_hapi_fhir(allergy_id, "AllergyIntolerance")