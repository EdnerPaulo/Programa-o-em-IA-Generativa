from typing import Generic, TypeVar, List, Optional
from uuid import UUID
from sqlmodel import Session, select

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def add(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_id(self, id: UUID) -> Optional[T]:
        return self.session.get(self.model, id)

    def list_all(self) -> List[T]:
        statement = select(self.model)
        return list(self.session.exec(statement).all())