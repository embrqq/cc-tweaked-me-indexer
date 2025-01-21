from typing import Dict, Any

from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy import func
from sqlalchemy.orm import (
    DeclarativeMeta,
    Mapped,
    declarative_base,
)


# Modifies the DeclarativeMeta default type used in declarative_base
# to capture custom tags to store in table info. Used by Alembic when
# generating commands to create migrations.
class BaseMeta(DeclarativeMeta):
    def __init__(self, name, bases, d):
        skip_autogenerate = d.pop("__skip_autogenerate__", False)
        super(BaseMeta, self).__init__(name, bases, d)
        if skip_autogenerate is True and self.__table__ is not None:
            self.__table__.info["skip_autogenerate"] = True


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata, metaclass=BaseMeta)


class UpdatedAtMixin:
    # Timestamp marking when this entry was last updated
    version_timestamp: Mapped[datetime] = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    def to_dict(self) -> Dict[str, Any]:
        return {"version_timestamp": self.version_timestamp}


class ItemStore(Base, UpdatedAtMixin):
    __tablename__ = "item_store"
    _pk_constraint = PrimaryKeyConstraint("item_id")
    __table_args__ = (_pk_constraint,)

    item_id: Mapped[str] = Column(String(256), nullable=False)
    item_count: Mapped[int] = Column(Integer, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "item_count": self.item_count,
            **UpdatedAtMixin.to_dict(self),
        }
