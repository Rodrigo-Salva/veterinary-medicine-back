from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.domain.entities.hospitalization import Hospitalization, Cage, VitalSignRecord
from app.domain.ports.hospitalization_repository import HospitalizationRepository
from app.infrastructure.adapters.db.models_hospital import CageModel, HospitalizationModel, VitalSignModel

class SqlAlchemyHospitalizationRepository(HospitalizationRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_cage(self, cage: Cage) -> Cage:
        db_cage = self.db.query(CageModel).filter(CageModel.id == cage.id).first()
        if not db_cage:
            db_cage = CageModel(id=cage.id, name=cage.name)
        db_cage.is_occupied = cage.is_occupied
        db_cage.current_pet_id = cage.current_pet_id
        self.db.add(db_cage)
        self.db.commit()
        return cage

    def get_cages(self) -> List[Cage]:
        db_cages = self.db.query(CageModel).all()
        results = []
        for c in db_cages:
            h_id = None
            if c.is_occupied and c.current_pet_id:
                active_h = self.db.query(HospitalizationModel).filter(
                    HospitalizationModel.cage_id == c.id,
                    HospitalizationModel.status == "Active"
                ).first()
                if active_h: h_id = active_h.id
            results.append(Cage(
                id=c.id, name=c.name, is_occupied=c.is_occupied, 
                current_pet_id=c.current_pet_id, current_hospitalization_id=h_id
            ))
        return results

    def get_cage_by_id(self, cage_id: uuid.UUID) -> Optional[Cage]:
        c = self.db.query(CageModel).filter(CageModel.id == cage_id).first()
        if not c: return None
        h_id = None
        if c.is_occupied and c.current_pet_id:
            active_h = self.db.query(HospitalizationModel).filter(
                HospitalizationModel.cage_id == c.id,
                HospitalizationModel.status == "Active"
            ).first()
            if active_h: h_id = active_h.id
        return Cage(
            id=c.id, name=c.name, is_occupied=c.is_occupied, 
            current_pet_id=c.current_pet_id, current_hospitalization_id=h_id
        )

    def delete_cage(self, cage_id: uuid.UUID) -> bool:
        db_cage = self.db.query(CageModel).filter(CageModel.id == cage_id).first()
        if not db_cage: return False
        if db_cage.is_occupied:
            raise Exception("Cannot delete an occupied cage")
        self.db.delete(db_cage)
        self.db.commit()
        return True

    def save_hospitalization(self, h: Hospitalization) -> Hospitalization:
        db_h = self.db.query(HospitalizationModel).filter(HospitalizationModel.id == h.id).first()
        if not db_h:
            db_h = HospitalizationModel(
                id=h.id, pet_id=h.pet_id, cage_id=h.cage_id, 
                check_in_date=h.check_in_date, reason=h.reason, status=h.status
            )
        else:
            db_h.status = h.status
            db_h.check_out_date = h.check_out_date
        self.db.add(db_h)
        self.db.commit()
        return h

    def get_hospitalization_by_id(self, hosp_id: uuid.UUID) -> Optional[Hospitalization]:
        db_h = self.db.query(HospitalizationModel).filter(HospitalizationModel.id == hosp_id).first()
        if not db_h: return None
        vitals = self.get_vital_signs_by_hosp_id(hosp_id)
        return Hospitalization(
            id=db_h.id, pet_id=db_h.pet_id, cage_id=db_h.cage_id,
            check_in_date=db_h.check_in_date, check_out_date=db_h.check_out_date,
            reason=db_h.reason, status=db_h.status, vital_signs=vitals
        )

    def get_active_hospitalization_by_pet_id(self, pet_id: uuid.UUID) -> Optional[Hospitalization]:
        db_h = self.db.query(HospitalizationModel).filter(
            HospitalizationModel.pet_id == pet_id, HospitalizationModel.status == "Active"
        ).first()
        return self.get_hospitalization_by_id(db_h.id) if db_h else None

    def save_vital_sign(self, v: VitalSignRecord) -> VitalSignRecord:
        db_v = VitalSignModel(
            id=v.id, hospitalization_id=v.hospitalization_id, timestamp=v.timestamp,
            temperature=v.temperature, heart_rate=v.heart_rate,
            respiratory_rate=v.respiratory_rate, notes=v.notes
        )
        self.db.add(db_v)
        self.db.commit()
        return v

    def get_vital_signs_by_hosp_id(self, hosp_id: uuid.UUID) -> List[VitalSignRecord]:
        db_v = self.db.query(VitalSignModel).filter(VitalSignModel.hospitalization_id == hosp_id).all()
        return [VitalSignRecord(
            id=v.id, hospitalization_id=v.hospitalization_id, timestamp=v.timestamp,
            temperature=v.temperature, heart_rate=v.heart_rate,
            respiratory_rate=v.respiratory_rate, notes=v.notes
        ) for v in db_v]
