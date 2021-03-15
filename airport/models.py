from django.db import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence

# SQLAlchemy models
Base = declarative_base()

class Airport(Base):
    __tablename__ = 'airport'

    # Columns
    id = Column(Integer, Sequence('air_id_seq'), primary_key=True)
    name = Column(String(256), nullable=False)
    airport_code = Column(String(20), nullable=False)
    location = Column(String, nullable=False)

    def __repr__(self):
        """String representation of this class"""
        return f"<Airport(id={str(self.id)}, name={self.name})>"