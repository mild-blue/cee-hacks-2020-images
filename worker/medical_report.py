from dataclasses import dataclass
from typing import Optional

from patient_data import PatientData


@dataclass
class MedicalReport:
    """
    Attributes:
    issuing_doctor: Name of the doctor who issued the medical report.
    date_of_issue: Date of the medical checkup.
    patient_data: Information about the patient.
    issuing_institution: The institution the medical report was issued by. Usually a hospital, medical center etc.
    date_next_checkup: Recommended next checkup, if available.
    subjective: Subjective status description, what the patient is reporting.
    objective: Objective status description, what the doctor found.
    summary: Summary of the medical report.
    recommendation: Recommended next actions for the patient.
    other: Notes, results from laboratory, previous checkups etc.
    """
    issuing_doctor: str
    date_of_issue: str
    patient_data: PatientData
    issuing_institution: Optional[str] = None
    date_next_checkup: Optional[str] = None
    subjective: Optional[str] = None
    objective: Optional[str] = None
    summary: Optional[str] = None
    recommendation: Optional[str] = None
    other: Optional[str] = None
