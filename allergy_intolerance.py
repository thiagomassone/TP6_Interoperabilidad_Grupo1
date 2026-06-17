from fhir.resources.allergyintolerance import AllergyIntolerance


def create_allergy_intolerance_resource(
    patient_id,
    substance_code=None,
    substance_display=None,
    clinical_status="active",
    verification_status="confirmed",
    allergy_type="allergy",
    category="medication",
    criticality="high",
    reaction_manifestation_code=None,
    reaction_manifestation_display=None,
    reaction_severity=None,
    note=None,
):
    """
    Crea un recurso FHIR AllergyIntolerance (R4 - fhir.resources 6.x).

    Parámetros
    ----------
    patient_id : str
        ID lógico del paciente en el servidor HAPI FHIR.
    substance_code : str
        Código SNOMED CT de la sustancia causante.
    substance_display : str
        Nombre legible de la sustancia.
    clinical_status : str
        Estado clínico: 'active' | 'inactive' | 'resolved'.
    verification_status : str
        Estado de verificación: 'unconfirmed' | 'confirmed' | 'refuted' | 'entered-in-error'.
    allergy_type : str
        Tipo: 'allergy' | 'intolerance'.
    category : str
        Categoría: 'food' | 'medication' | 'environment' | 'biologic'.
    criticality : str
        Criticidad: 'low' | 'high' | 'unable-to-assess'.
    reaction_manifestation_code : str
        Código SNOMED CT de la manifestación de la reacción.
    reaction_manifestation_display : str
        Nombre legible de la manifestación.
    reaction_severity : str
        Severidad: 'mild' | 'moderate' | 'severe'.
    note : str
        Nota adicional en texto libre.
    """

    data = {
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                    "code": clinical_status,
                    "display": clinical_status.capitalize(),
                }
            ]
        },
        "verificationStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                    "code": verification_status,
                    "display": verification_status.capitalize(),
                }
            ]
        },
        "type": allergy_type,
        "category": [category],
        "criticality": criticality,
        "patient": {"reference": f"Patient/{patient_id}"},
    }

    # Sustancia
    if substance_code or substance_display:
        code_entry = {}
        if substance_code:
            code_entry["coding"] = [
                {
                    "system": "http://snomed.info/sct",
                    "code": substance_code,
                    "display": substance_display or "",
                }
            ]
        if substance_display:
            code_entry["text"] = substance_display
        data["code"] = code_entry

    # Reacción — en R4, manifestation es CodeableConcept directo
    if reaction_manifestation_code or reaction_manifestation_display:
        manifestation = {}
        if reaction_manifestation_code:
            manifestation["coding"] = [
                {
                    "system": "http://snomed.info/sct",
                    "code": reaction_manifestation_code,
                    "display": reaction_manifestation_display or "",
                }
            ]
        if reaction_manifestation_display:
            manifestation["text"] = reaction_manifestation_display

        reaction = {"manifestation": [manifestation]}
        if reaction_severity:
            reaction["severity"] = reaction_severity

        data["reaction"] = [reaction]

    # Nota
    if note:
        data["note"] = [{"text": note}]

    return AllergyIntolerance(**data)