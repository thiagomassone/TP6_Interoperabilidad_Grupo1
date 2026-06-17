from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier


# Crear el recurso FHIR de paciente con parámetros opcionales
def create_patient_resource(family_name=None, given_name=None, birth_date=None, gender=None, phone=None, dni=None):
    patient = Patient()

    # Agregar el DNI como identifier si está disponible
    if dni:
        identifier = Identifier()
        identifier.system = "http://www.renaper.gob.ar/dni"
        identifier.value = str(dni)
        patient.identifier = [identifier]

    # Agregar el nombre del paciente si está disponible
    if family_name or given_name:
        name = HumanName()
        if family_name:
            name.family = family_name
        if given_name:
            name.given = [given_name]
        patient.name = [name]

    # Agregar la fecha de nacimiento si está disponible
    if birth_date:
        patient.birthDate = birth_date

    # Agregar el género si está disponible
    if gender:
        patient.gender = gender

    # Agregar información de contacto si está disponible
    if phone:
        contact = ContactPoint()
        contact.system = "phone"
        contact.value = phone
        contact.use = "mobile"
        patient.telecom = [contact]

    return patient
