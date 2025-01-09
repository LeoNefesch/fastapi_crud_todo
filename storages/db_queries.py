from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar, List, Optional, Dict

from sqlalchemy.orm import Session

TEntity = TypeVar("TEntity")
TCreate = TypeVar("TCreate")


class TodoService(ABC, Generic[TEntity, TCreate]):
    """Абстрактный класс для операций с БД."""

    @abstractmethod
    def create(self, create_data: TCreate) -> TEntity:
        """Создание новой сущности."""
        pass

    @abstractmethod
    def get_all(self) -> List[TEntity]:
        """Получение всех сущностей."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        """Получение сущности по ID."""
        pass

    @abstractmethod
    def update_fields(self, entity_id: int, fields: Dict) -> Optional[TEntity]:
        """Обновление сущности по ID."""
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Удаление сущности по ID."""
        pass


class SQLiteTodoService(TodoService[TEntity, TCreate]):
    def __init__(self, db: Session, model: Type[TEntity]):
        """
        :param db: Сессия SQLAlchemy.
        :param model: Модель SQLAlchemy, с которой работает сервис.
        """
        self.db = db
        self.model = model

    def create(self, create_data: TCreate) -> TEntity:
        new_entity = self.model(**create_data.model_dump())  # type: ignore[attr-defined]
        self.db.add(new_entity)
        self.db.commit()
        self.db.refresh(new_entity)
        return new_entity

    def get_all(self) -> List[TEntity]:
        return self.db.query(self.model).all()

    def get_by_id(self, entity_id: int) -> Optional[TEntity]:
        return self.db.query(self.model).filter(self.model.id == entity_id).first()  # type: ignore[attr-defined]

    def update_fields(self, entity_id: int, fields: Dict) -> Optional[TEntity]:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        for key, value in fields.items():
            if value is not None:
                setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.get_by_id(entity_id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False
