import requests
from patient import create_patient_resource

HAPI_BASE_URL = "http://hapi.fhir.org/baseR4"
HEADERS_POST = {"Content-Type": "application/fhir+json"}
HEADERS_GET  = {"Accept": "application/fhir+json"}


# Enviar un recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource, resource_type):
    url = f"{HAPI_BASE_URL}/{resource_type}"
    resource_json = resource.json()
    response = requests.post(url, headers=HEADERS_POST, data=resource_json)

    if response.status_code == 201:
        print("Recurso creado exitosamente")
        return response.json()["id"]
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None


# Leer un recurso por ID
def get_resource_from_hapi_fhir(resource_id, resource_type):
    url = f"{HAPI_BASE_URL}/{resource_type}/{resource_id}"
    response = requests.get(url, headers=HEADERS_GET)

    if response.status_code == 200:
        resource = response.json()
        print(resource)
        return resource
    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())
        return None


# Buscar pacientes por número de documento (DNI)
def search_patient_by_dni(dni):
    """
    Busca pacientes cuyo identifier coincida con el DNI proporcionado.
    Utiliza el sistema RENAPER como identificador oficial argentino.
    """
    url = f"{HAPI_BASE_URL}/Patient"
    params = {
        "identifier": f"http://www.renaper.gob.ar/dni|{dni}"
    }
    response = requests.get(url, headers=HEADERS_GET, params=params)

    if response.status_code == 200:
        bundle = response.json()
        total = bundle.get("total", 0)
        print(f"Pacientes encontrados: {total}")

        entries = bundle.get("entry", [])
        for entry in entries:
            patient = entry.get("resource", {})
            print(f"  ID: {patient.get('id')}")
            names = patient.get("name", [])
            if names:
                print(f"  Nombre: {names[0].get('given', [])} {names[0].get('family', '')}")
        return bundle
    else:
        print(f"Error en la búsqueda: {response.status_code}")
        print(response.json())
        return None
