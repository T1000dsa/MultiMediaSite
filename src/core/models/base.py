from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped,
    mapped_column,
    declared_attr
    )

class Base(DeclarativeBase):

    #@declared_attr.directive
    #def __tablename__(cls):
    #    return cls.__name__.lower()

    id:Mapped[int] = mapped_column(primary_key=True)
