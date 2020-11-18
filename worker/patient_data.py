from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Address:
    street: str
    descriptive_street_number: int
    orientation_street_number: str
    city: str
    postal_code: int


@dataclass
class PatientData:
    """
    Attributes
    given_names:
    family_name:
    date_of_birth:
    personal_number: "Rodne cislo".
    insurance_company: Name of the insurance company.
    insurance_company_code: Numerical code of the insurance company.
    address:
    family_anamnesis: Relevant diseases in the family.
    personal_anamnesis: Medical history of the patient.
    professional_anamnesis: Occupation of the patient.
    social_anamnesis: Family status of the patient.
    pharmacological_anamnesis: Any medications the patient is taking.
    allergological_anamnesis: Any allergies the patient suffers with.
    injury_anamnesis: Previous injuries of the patient.
    """
    given_names: List[str]
    family_name: str
    date_of_birth: Optional[str] = None
    personal_number: Optional[int] = None
    insurance_company: Optional[str] = None
    insurance_company_code: Optional[int] = None
    address: Optional[Address] = None
    family_anamnesis: Optional[str] = None
    personal_anamnesis: Optional[str] = None
    professional_anamnesis: Optional[str] = None
    social_anamnesis: Optional[str] = None
    pharmacological_anamnesis: Optional[str] = None
    allergological_anamnesis: Optional[str] = None
    injury_anamnesis: Optional[str] = None
