from abc import abstractmethod, ABC

from sqlalchemy.orm import Session

import schemas


class IdentityRepository(ABC):
    @abstractmethod
    def get_identity(self, db: Session):
        pass
    @abstractmethod
    def create_identity(self, db: Session, identity: schemas.CreateIdentityCommand):
        pass