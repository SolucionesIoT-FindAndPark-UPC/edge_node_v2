from sqlalchemy.orm import Session

import models
import schemas

from ports.identity_repository import IdentityRepository


class IdentityMySqlRepository(IdentityRepository):
    def get_identity(self, db: Session):
        return db.query(models.Identity).first()
    def create_identity(self, db: Session, identity: schemas.CreateIdentityCommand):
        db_identity = models.Identity(id=identity.id)
        db.add(db_identity)
        db.commit()
        db.refresh(db_identity)
        return db_identity