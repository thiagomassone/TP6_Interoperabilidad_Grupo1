from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.allergyintolerancereaction import AllergyIntoleranceReaction
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from fhir.resources.annotation import Annotation
from fhir.resources.fhirtypes import DateTime


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
    Crea un recurso FHIR AllergyIntolerance.

    Parámetros
    ----------
    patient_id : str
        ID lógico del paciente en el servidor HAPI FHIR.
    substance_code : str
        Código SNOMED CT (u otro sistema) de la sustancia.
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

    allergy = AllergyIntolerance()

    # --- clinicalStatus (requerido) ---
    clinical_status_cc = CodeableConcept()
    clinical_status_coding = Coding()
    clinical_status_coding.system = (
        "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical"
    )
    clinical_status_coding.code = clinical_status
    clinical_status_coding.display = clinical_status.capitalize()
    clinical_status_cc.coding = [clinical_status_coding]
    allergy.clinicalStatus = clinical_status_cc

    # --- verificationStatus (requerido) ---
    verification_status_cc = CodeableConcept()
    verification_status_coding = Coding()
    verification_status_coding.system = (
        "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification"
    )
    verification_status_coding.code = verification_status
    verification_status_coding.display = verification_status.capitalize()
    verification_status_cc.coding = [verification_status_coding]
    allergy.verificationStatus = verification_status_cc

    # --- type (allergy / intolerance) ---
    allergy.type = allergy_type

    # --- category ---
    allergy.category = [category]

    # --- criticality ---
    allergy.criticality = criticality

    # --- code (sustancia) ---
    if substance_code or substance_display:
        code_cc = CodeableConcept()
        if substance_code:
            substance_coding = Coding()
            substance_coding.system = "http://snomed.info/sct"
            substance_coding.code = substance_code
            if substance_display:
                substance_coding.display = substance_display
            code_cc.coding = [substance_coding]
        if substance_display:
            code_cc.text = substance_display
        allergy.code = code_cc

    # --- patient (requerido) ---
    patient_ref = Reference()
    patient_ref.reference = f"Patient/{patient_id}"
    allergy.patient = patient_ref

    # --- reaction ---
    if reaction_manifestation_code or reaction_manifestation_display:
        reaction = AllergyIntoleranceReaction()

        manifestation_cc = CodeableConcept()
        if reaction_manifestation_code:
            manifestation_coding = Coding()
            manifestation_coding.system = "http://snomed.info/sct"
            manifestation_coding.code = reaction_manifestation_code
            if reaction_manifestation_display:
                manifestation_coding.display = reaction_manifestation_display
            manifestation_cc.coding = [manifestation_coding]
        if reaction_manifestation_display:
            manifestation_cc.text = reaction_manifestation_display

        reaction.manifestation = [manifestation_cc]

        if reaction_severity:
            reaction.severity = reaction_severity

        allergy.reaction = [reaction]

    # --- note ---
    if note:
        annotation = Annotation()
        annotation.text = note
        allergy.note = [annotation]

    return allergy
