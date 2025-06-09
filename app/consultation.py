import uuid

from .database import db

class Consultation:
    def __init__(self,record_id=None, patient_id=None, doctor_id=None, organization_id=None, transcript=None):
        self.record_id = record_id if record_id else uuid.uuid4().hex
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.organization_id = organization_id
        self.transcript = transcript
        self.top_5_disease = None
        self.prescribed_medicine = None
        self.transcribe_summary = None
        self._db = db

    def create(self):
        """
        Creates a new consultation record.
        Returns:
            record_id: If the consultation record is successfully created.
        """
        record_id = self._db.create_consultation_record(self.record_id, self.patient_id, self.doctor_id, self.organization_id)
        return record_id