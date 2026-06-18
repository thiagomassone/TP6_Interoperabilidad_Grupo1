# TP6 – Interoperabilidad FHIR | Grupo 1

Trabajo Práctico N°6 de Informática Médica (Bioingeniería – ITBA).  
Implementación del recurso **AllergyIntolerance** sobre un servidor HAPI FHIR público usando Python.

---

## Integrantes

| Nombre | Padrón |
|---|---|
| Francisco Gagna | 55224 |
| Thiago Massone | 60035 |
| Mateo Chaul | 61036 |

**Fecha:** 17/06/2026

---

## Clonar el repositorio

```bash
git clone https://github.com/thiagomassone/TP6_Interoperabilidad_Grupo1.git
cd TP6_Interoperabilidad_Grupo1
```

---

## Requisitos

- Python 3.11+
- Las dependencias del proyecto:

```bash
pip install fhir.resources==6.5.0 pydantic==1.10.21 requests
```

---

## Archivos

| Archivo | Descripción |
|---|---|
| `base.py` | Envía (POST) y trae (GET) recursos al endpoint de HAPI FHIR. Incluye búsqueda de pacientes por DNI. |
| `patient.py` | Crea el recurso FHIR `Patient` con parámetros opcionales. |
| `allergy_intolerance.py` | Crea el recurso FHIR `AllergyIntolerance` con todos sus campos. |
| `workflow.py` | Script que ejecuta las tres actividades de la consigna de forma explícita (legacy). |
| `menu.py` | Menú interactivo por terminal para crear pacientes y consultar alergias. |

---

## Uso

### Workflow (actividades del TP)

```bash
python workflow.py
```

Ejecuta las tres actividades en orden:
- **3a** – Crea un paciente con DNI como identifier y lo lee
- **3b** – Busca el paciente creado por DNI
- **3c** – Crea un recurso `AllergyIntolerance` asociado al paciente

### Menú interactivo

```bash
python menu.py
```

Permite:
1. **Crear paciente** – ingreso de datos con validación de campos (género, fecha, DNI, teléfono)
2. **Buscar paciente por DNI** – muestra los datos del paciente y permite consultar sus alergias registradas con sus URLs en HAPI FHIR

---

## Recurso AllergyIntolerance

Registra alergias e intolerancias de un paciente a sustancias como medicamentos, alimentos o agentes ambientales. Permite que cualquier sistema de salud conozca los riesgos del paciente antes de prescribir o administrar un tratamiento.

### Campos principales

| Campo | Requerido | Descripción |
|---|---|---|
| `clinicalStatus` | ✓ | Estado actual: `active`, `inactive`, `resolved` |
| `verificationStatus` | ✓ | Confirmación: `unconfirmed`, `confirmed`, `refuted` |
| `patient` | ✓ | Referencia al recurso `Patient` |
| `type` | | Tipo: `allergy` o `intolerance` |
| `category` | | Categoría: `medication`, `food`, `environment`, `biologic` |
| `criticality` | | Riesgo potencial: `low`, `high`, `unable-to-assess` |
| `code` | | Sustancia causante (codificada en SNOMED CT) |
| `reaction` | | Lista de episodios de reacción (manifestación + severidad) |

### Sub-elemento reaction

| Campo | Descripción |
|---|---|
| `manifestation` | Síntoma observado, requerido (codificado en SNOMED CT) |
| `severity` | Severidad: `mild`, `moderate`, `severe` |
| `substance` | Sustancia específica de la reacción |
| `description` | Texto libre descriptivo |

---

## Servidor HAPI FHIR público

Endpoint base: `http://hapi.fhir.org/baseR4`

Recursos creados durante el desarrollo:

- Patient: http://hapi.fhir.org/baseR4/Patient/137001175
- AllergyIntolerance: http://hapi.fhir.org/baseR4/AllergyIntolerance/137001179
